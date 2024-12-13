import requests

from fastapi import HTTPException, Request
from datetime import timedelta
from jose import ExpiredSignatureError, JWTError
from sqlmodel import Session

from database.repository import UserRepositoryMeta, UserRepository, ImageRepositoryMeta, ImageRepository, TokenRepositoryMeta, TokenRepository
from database.schema import TokenData, UserInfoGoogle, Token, UserLogin, UserResponse, UserRegister
from database.schema.auth_schema import TokenType, RefreshInput, GoogleToken
from service import AuthServiceMeta
from model import Users, IssuedAccessToken, IssuedRefreshToken, Images
from utils import get_password_hash, verify_password, create_refresh_token, decode_token
from utils.hashing import generate_device_id
from utils.token_utils import create_access_token
from config import EXPIRATION_TIME, REFRESH_TOKEN_EXPIRATION_TIME


class AuthService(AuthServiceMeta):

    def __init__(self, session:Session, request: Request, user: Users = Users()):
        self.session = session
        self._user_repository : UserRepositoryMeta = UserRepository(self.session)
        self._token_repository: TokenRepositoryMeta = TokenRepository(self.session)
        self._image_repository :ImageRepositoryMeta = ImageRepository(self.session)
        self._user = user
        self._device_id = generate_device_id(
            user_agent=request.headers.get("user-agent", "unknown"),
            ip_address=request.client.host
        )

    def _issue_token(self, data: TokenData):
        return (
            create_access_token(data, timedelta(hours=EXPIRATION_TIME), self._device_id, self.session),
            create_refresh_token(data, timedelta(days=REFRESH_TOKEN_EXPIRATION_TIME), self._device_id, self.session)
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

            db_access_token = self._token_repository.access_token_exist(user.id, self._device_id)
            if db_access_token:
                self._token_repository.deactivate_access_token(db_access_token)

            db_refresh_token = self._token_repository.refresh_token_exist(user.id, self._device_id)
            if db_refresh_token:
                self._token_repository.revoke_refresh_token(db_refresh_token)

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
                image_id = self._image_repository.create(Images(image_path=user_info.picture))
                db_user = Users(email=user_info.email, password='-', username=username, full_name=user_info.name, profile_img=image_id)
                self._user_repository.add(db_user)
            except:
                raise HTTPException(status_code=400, detail=str('Masih belum bisa'))
        else:
            db_user = self._user_repository.get_by_email(user_info.email)

        db_access_token = self._token_repository.access_token_exist(db_user.id, self._device_id)
        if db_access_token:
            self._token_repository.deactivate_access_token(db_access_token)

        db_refresh_token = self._token_repository.refresh_token_exist(db_user.id, self._device_id)
        if db_refresh_token:
            self._token_repository.revoke_refresh_token(db_refresh_token)

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

        if db_token and db_token.revoked:
            self._token_repository.deactivate_all_token(user.id, db_token.device_id)

        if db_token and not db_token.revoked and db_token.device_id == self._device_id:
            db_access_token = self._token_repository.access_token_exist(user.id, self._device_id)
            db_token.revoked = True
            self.session.add(db_token)
            self.session.commit()
            token_data = TokenData(id=str(user.id), username=user.username)
            access_token, refresh_token = self._issue_token(token_data)
            if db_access_token:
                self._token_repository.deactivate_access_token(db_access_token)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }

        raise HTTPException(status_code=403, detail='Invalid refresh token.')

    def logout(self, jti: str) -> bool:
        token = self.session.get(IssuedAccessToken, jti)
        if token:
            db_refresh_token = self._token_repository.refresh_token_exist(token.user_id, self._device_id)
            token.status = False
            self.session.add(token)
            self.session.commit()
            if db_refresh_token:
                self._token_repository.revoke_refresh_token(db_refresh_token)
            return True
        return False

    def __get_user_info(self, token: str) -> UserInfoGoogle:
        user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                                 headers={"Authorization": f"Bearer {token}"})
        payload = user_info.json()
        return UserInfoGoogle(**payload)
