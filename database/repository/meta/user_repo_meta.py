from abc import abstractmethod

from model import Users

class UserRepositoryMeta:
    @abstractmethod
    def add(self, model: Users) -> Users:
        pass

    @abstractmethod
    def edit(self, model: Users, _id: str) -> Users:
        pass

    @abstractmethod
    def get_by_id(self, _id: str) -> Users:
        pass

    @abstractmethod
    def get_by_email(self, _email: str) -> Users:
        pass

    @abstractmethod
    def get_by_username(self, _username: str) -> Users:
        pass