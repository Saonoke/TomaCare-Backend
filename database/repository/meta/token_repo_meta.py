from abc import abstractmethod

from model import IssuedAccessToken, IssuedRefreshToken

class TokenRepositoryMeta:
    @abstractmethod
    def access_token_exist(self, user_id: int, device_id: str) -> bool|IssuedAccessToken:
        pass

    @abstractmethod
    def deactivate_access_token(self, token: IssuedAccessToken) -> bool:
        pass

    @abstractmethod
    def revoke_refresh_token(self, token: IssuedRefreshToken) -> bool:
        pass

    @abstractmethod
    def refresh_token_exist(self, user_id: int, device_id: str) -> bool|IssuedRefreshToken:
        pass

    @abstractmethod
    def deactivate_all_token(self, _user_id: int, _device_id: str):
        pass