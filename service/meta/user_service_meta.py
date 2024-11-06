from abc import abstractmethod

from sqlmodel import Session

from model import Users


class UserServiceMeta:

    @abstractmethod
    def get(self, _id: int) -> Users:
        pass

    @abstractmethod
    def edit(self, user_data: Users, _id: int) -> Users:
        pass

    @abstractmethod
    def change_password(self, _old_pass: str, _new_pass: str, _id: int):
        pass

    @abstractmethod
    def create_password(self, _pass: str, _id: int):
        pass