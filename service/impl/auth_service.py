import requests

from fastapi import Depends, HTTPException
from datetime import timedelta
from sqlmodel import Session
from database.repository import UserRepositoryMeta, UserRepository
from database.schema import TokenData, UserInfoGoogle, Token, UserLogin, UserResponse, UserRegister
from service import AuthServiceMeta
from model import Users
from utils import get_password_hash, verify_password
from utils.token_utils import create_access_token
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_REDIRECT_URL, GOOGLE_CLIENT_SECRET, EXPIRATION_TIME


class AuthService(AuthServiceMeta):
    

    def __init__(self, session:Session):
        self.session = session
        self._user_repository : UserRepositoryMeta = UserRepository(self.session)

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

    def authenticate_user(self, login_data: UserLogin) -> UserResponse:
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
            return create_access_token(token_data, timedelta(hours=EXPIRATION_TIME))
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise e

    def registered_email(self, email: str) -> bool:
        user = self._user_repository.get_by_email(email)

        if not user:
            return False
        return True

    def authenticate_google(self, code: str) -> Token:
        token_url = "https://accounts.google.com/o/oauth2/token"
        data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_CLIENT_REDIRECT_URL,
            "grant_type": "authorization_code",
        }
        response = requests.post(token_url, data=data)
        access_token = response.json().get("access_token")

        user_info = self.__get_user_info(access_token)
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

        return create_access_token(token_data, timedelta(hours=EXPIRATION_TIME))


    def refresh_token(self, token: str):
        pass

    def __get_user_info(self, token: str) -> UserInfoGoogle:
        user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                                 headers={"Authorization": f"Bearer {token}"})
        payload = user_info.json()
        return UserInfoGoogle(**payload)
