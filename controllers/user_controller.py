from fastapi import Depends, HTTPException, Request
from sqlmodel import Session

from database.database import get_session
from database.schema import UserLogin, UserRegister, UserResponse, Token, TokenData

from model import Users
from controllers.base_controller import BaseController
from service.meta import UserServiceMeta
from service.impl import UserService

class UserController(BaseController):
    _user_service: UserServiceMeta

    def __init__(self, session: Session):
        self._user_service: UserServiceMeta = UserService(session)

    def get(self, request: Request) -> Users:
        try:
            return self._user_service.get(request.state.user.id)
        except HTTPException as e:
            raise e
        except Exception as e:
            return self.ise(e)

    def update(self, request: Request, user_model: Users) -> Users:
        try:
            return self._user_service.edit(user_model, request.state.user.id)
        except HTTPException as e:
            raise e
        except Exception as e:
            return self.ise(e)

    def change_password(self, request: Request, _old_pass: str, _new_pass: str) -> Users:
        try:
            return self._user_service.change_password(_old_pass, _new_pass, request.state.user.id)
        except HTTPException as e:
            raise e
        except Exception as e:
            return self.ise(e)

    def create_password(self, request: Request, _pass: str) -> Users:
        try:
            return self._user_service.create_password(_pass, request.state.user.id)
        except HTTPException as e:
            raise e
        except Exception as e:
            return self.ise(e)