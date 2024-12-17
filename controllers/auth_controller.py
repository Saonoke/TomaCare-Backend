from fastapi import Depends, HTTPException, Request
from database.database import get_session
from sqlmodel import Session
from database.schema import UserLogin, UserRegister, Token, TokenData
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_REDIRECT_URL
from model import Users
from controllers.base_controller import BaseController
from service import AuthServiceMeta
from service import AuthService

class AuthController(BaseController):
    _user_service: AuthServiceMeta

    def __init__(self,request: Request, session: Session):
        self._user_service: AuthServiceMeta = AuthService(session, request)

    def register(self, user: UserRegister) -> UserRegister:
        try:
            data = self._user_service.create_user(user)
       
            return data
        except Exception as e:
            return self.ise(e)

    def login(self, user: UserLogin) -> Token:
        try:
            return self._user_service.authenticate_user(user)
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            return self.ise(e)

    def logout(self, jti: str) -> dict[str, bool]:
        return {
            'success': self._user_service.logout(jti)
        }

    def refresh_token(self, refresh_token: str) -> Token:
        try:
            return self._user_service.update_token(refresh_token)
        except HTTPException as e:
            raise e
        except Exception as e:
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