from sqlmodel import select, Session

from database.repository.meta import TokenRepositoryMeta
from model import IssuedAccessToken, IssuedRefreshToken, Users


class TokenRepository(TokenRepositoryMeta):
    def __init__(self, session:Session):
        self.session = session

    def deactivate_access_token(self, token: IssuedAccessToken):
        try:
            token.status = 0
            self.session.add(token)
            self.session.commit()
            return True
        except:
            return False

    def revoke_refresh_token(self, token: IssuedRefreshToken):
        try:
            token.revoked = 1
            self.session.add(token)
            self.session.commit()
            return True
        except:
            return False

    def access_token_exist(self, _user_id: int, _device_id: str) -> bool|IssuedAccessToken:
        stm = (
            select(IssuedAccessToken)
            .join(Users, Users.id == IssuedAccessToken.user_id)
            .where(Users.id == _user_id)
            .where(IssuedAccessToken.device_id == _device_id)
            .where(IssuedAccessToken.status == True)
        )
        result = self.session.exec(stm)
        res = result.first()
        if res is None:
            return False
        return res

    def refresh_token_exist(self, _user_id: int, _device_id: str) -> bool:
        stm = (
            select(IssuedRefreshToken)
            .join(Users, Users.id == IssuedRefreshToken.user_id)
            .where(Users.id == _user_id)
            .where(IssuedRefreshToken.device_id == _device_id)
            .where(IssuedRefreshToken.revoked == False)
        )
        result = self.session.exec(stm)
        res = result.first()
        if res is None:
            return False
        return res

    def deactivate_all_token(self, _user_id: int, _device_id: str):
        access_token = self.access_token_exist(_user_id, _device_id)
        refresh_token = self.refresh_token_exist(_user_id, _device_id)

        self.deactivate_access_token(access_token)
        self.revoke_refresh_token(refresh_token)