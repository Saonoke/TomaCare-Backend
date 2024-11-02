from fastapi import Depends, HTTPException
from database.schema import UserLogin, UserRegister, UserResponse, Token, TokenData
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_REDIRECT_URL
from model import Users
from controllers.base_controller import BaseController
from service.meta import AuthServiceMeta
from service.impl import AuthService

class AuthController(BaseController):
    _user_service: AuthServiceMeta

    def __init__(self, log_service: AuthServiceMeta = Depends(AuthService)):
        self._user_service = log_service

    def register(self, user: UserRegister) -> UserResponse:
        try:
            return self._user_service.create_user(user)
        except Exception as e:
            return self.ise(e)

    def login(self, user: UserLogin) -> UserResponse:
        try:
            return self._user_service.authenticate_user(user)
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            return self.ise(e)

    @staticmethod
    def google_url() -> dict[str:str]:
        return {
            "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_CLIENT_REDIRECT_URL}&scope=openid%20profile%20email&access_type=offline"
        }

    def google_token(self, code: str) -> Token:
        try:
            return self._user_service.authenticate_google(code)
        except Exception as e:
            return self.ise(e)

    @staticmethod
    def userinfo(user: Users) -> TokenData:
        if user is None:
            raise HTTPException(status_code=401, detail='Authentication Failed')
        return user