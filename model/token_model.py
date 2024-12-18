from sqlmodel import SQLModel, Field


class IssuedAccessToken(SQLModel, table=True):
    jti: str = Field(primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    device_id: str
    exp: int
    status: bool

class IssuedRefreshToken(SQLModel, table=True):
    jti: str = Field(primary_key=True)
    user_id: int  = Field(default=None, foreign_key="users.id")
    device_id: str
    exp: int
    revoked: bool