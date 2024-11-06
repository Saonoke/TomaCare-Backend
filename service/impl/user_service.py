from fastapi import Depends, HTTPException
from sqlmodel import Session

from database.repository import UserRepository, UserRepositoryMeta
from model import Users
from service.meta import UserServiceMeta
from utils.hashing import get_password_hash, verify_password

class UserService(UserServiceMeta):
    _user_repository = UserRepositoryMeta

    def __init__(self, session: Session):
        self._user_repository = UserRepository(session)

    def get(self, _id: int):
        try:
            user = self._user_repository.get_by_id(_id)
            if user is None:
                raise HTTPException(status_code=403, detail="User not found.")
            return user
        except HTTPException as e:
            raise e

    def edit(self, user_data: Users, _id: int) -> Users:
        try:
            user_exist = self._user_repository.get_by_email(user_data.email)
            if user_exist and (user_exist.id != _id):
                raise HTTPException(status_code=400, detail="User with this email already exists.")

            user_exist = self._user_repository.get_by_username(user_data.username)
            if user_exist and (user_exist.id != _id):
                raise HTTPException(status_code=400, detail="User with this username already exists.")
            return self._user_repository.edit(user_data, _id)

        except HTTPException as e:
            raise e

    def change_password(self, _old_pass: str, _new_pass: str, _id: int):
        try:
            user = self._user_repository.get_by_id(_id)
            if not user:
                raise HTTPException(status_code=403, detail="User not found.")

            if not verify_password(_old_pass, user.password):
                raise HTTPException(status_code=400, detail="Invalid password.")

            new_pass = get_password_hash(_new_pass)
            user.password = new_pass

            return self._user_repository.edit(user, _id)

        except HTTPException as e:
            raise e

    def create_password(self, _pass: str, _id: int):
        try:
            user = self._user_repository.get_by_id(_id)

            if user.password != '-':
                raise HTTPException(status_code=400, detail="Password already set!")

            new_pass = get_password_hash(_pass)
            user.password = new_pass

            return self._user_repository.edit(user, _id)

        except HTTPException as e:
            raise e
