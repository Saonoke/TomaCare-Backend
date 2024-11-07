from abc import abstractmethod

from database.schema import UserResponse, UserRegister, UserLogin, Token, UserInfoGoogle

class AuthServiceMeta:

    @abstractmethod
    def create_user(self, user: UserRegister) -> UserResponse:
        pass

    @abstractmethod
    def authenticate_user(self, login_data: UserLogin) -> UserResponse:
        pass

    @abstractmethod
    def registered_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def authenticate_google(self, code: str) -> Token:
        pass

    @abstractmethod
    def refresh_token(self, token: str):
        pass

    @abstractmethod
    def __get_user_info(self, token: str) -> UserInfoGoogle:
        pass