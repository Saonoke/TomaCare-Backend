from model import IssuedAccessToken, IssuedRefreshToken
from sqlmodel import Session, select

class token_seeder():
    def __init__(self,session:Session):
        self.session = session
    def clear(self):
        issuedAccessToken = self.session.exec(select(IssuedAccessToken)).all()
        issuedRefreshToken = self.session.exec(select(IssuedRefreshToken)).all()

        for accessToken,refreshToken in zip(issuedAccessToken, issuedRefreshToken):
            self.session.delete(accessToken)
            self.session.delete(refreshToken)
        self.session.commit()