import requests

from fastapi import HTTPException
from datetime import timedelta

from jose import ExpiredSignatureError, JWTError
from sqlmodel import Session
from database.repository import UserRepositoryMeta, UserRepository
from database.schema import TokenData, UserInfoGoogle, Token, UserLogin, UserResponse, UserRegister
from database.schema.auth_schema import TokenType, RefreshInput, GoogleToken
from service import AuthServiceMeta
from model import Users, IssuedAccessToken, IssuedRefreshToken
from utils import get_password_hash, verify_password, create_refresh_token, decode_token
from utils.token_utils import create_access_token
from config import EXPIRATION_TIME, REFRESH_TOKEN_EXPIRATION_TIME


class AuthService(AuthServiceMeta):

    def __init__(self, session:Session, user: Users = Users()):
        self.session = session
        self._user_repository : UserRepositoryMeta = UserRepository(self.session)
        self._user = user

    def _issue_token(self, data: TokenData):
        return (
            create_access_token(data, timedelta(hours=EXPIRATION_TIME), self.session),
            create_refresh_token(data, timedelta(days=REFRESH_TOKEN_EXPIRATION_TIME), self.session)
        )

    def create_user(self, user: UserRegister) -> UserResponse:
        try:
            if self._user_repository.get_by_email(user.email):
                raise HTTPException(status_code=400, detail="User with this email already exists.")
            if self._user_repository.get_by_username(user.username):
                raise HTTPException(status_code=400, detail="User with this username already exists.")

            hashed_password = get_password_hash(user.password)
            user = Users(email=user.email, password=hashed_password, username=user.username, full_name=user.full_name)
            self._user_repository.add(user)

            return user
        except Exception as e:
            raise e

    def authenticate_user(self, login_data: UserLogin) -> Token:
        try:
            if '@' in login_data.email_or_username:
                user = self._user_repository.get_by_email(login_data.email_or_username)
            else:
                user = self._user_repository.get_by_username(login_data.email_or_username)
            if not user:
                raise HTTPException(status_code=400, detail="Invalid credentials")
            if not verify_password(login_data.password, user.password):
                raise HTTPException(status_code=400, detail="Invalid credentials")

            token_data = TokenData(id=str(user.id), username=user.username)

            access_token, refresh_token = self._issue_token(token_data)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise e

    def registered_email(self, email: str) -> bool:
        user = self._user_repository.get_by_email(email)

        if not user:
            return False
        return True

    def authenticate_google(self, google_access_token: GoogleToken) -> Token:
        try:
            user_info = self.__get_user_info(google_access_token.google_access_token)
        except Exception as e:
            raise HTTPException(status_code=401, detail='Invalid token!')

        if not self._user_repository.get_by_email(user_info.email):
            try:
                username = user_info.email.split('@')[0]
                db_user = Users(email=user_info.email, password='-', username=username, full_name=user_info.name)
                self._user_repository.add(db_user)
            except:
                raise HTTPException(status_code=400, detail=str('Masih belum bisa'))
        else:
            db_user = self._user_repository.get_by_email(user_info.email)

        token_data = TokenData(id=str(db_user.id), username=db_user.username)
        access_token, refresh_token = self._issue_token(token_data)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }


    def update_token(self, refresh_token: RefreshInput):
        try:
            payload = decode_token(refresh_token.refresh_token)
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired.')
        except JWTError:
            raise HTTPException(status_code=401, detail='Invalid refresh token.')

        if payload['type'] != TokenType.REFRESH.value:
            raise HTTPException(status_code=400, detail='Invalid token type.')

        user = self.session.get(Users, int(payload['user_id']))
        if not user:
            raise HTTPException(status_code=403, detail='Invalid user.')

        db_token = self.session.get(IssuedRefreshToken, payload['jti'])

        if db_token and not db_token.revoked:
            db_token.revoked = True
            self.session.add(db_token)
            self.session.commit()
            token_data = TokenData(id=str(user.id), username=user.username)
            access_token, refresh_token = self._issue_token(token_data)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }

        raise HTTPException(status_code=403, detail='Invalid refresh token.')

    def logout(self, jti: str) -> bool:
        token = self.session.get(IssuedAccessToken, jti)
        if token:
            token.status = False
            self.session.add(token)
            self.session.commit()
            return True
        return False

    def __get_user_info(self, token: str) -> UserInfoGoogle:
        user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                                 headers={"Authorization": f"Bearer {token}"})
        payload = user_info.json()
        return UserInfoGoogle(**payload)
