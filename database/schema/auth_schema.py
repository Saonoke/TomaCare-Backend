from enum import Enum

from pydantic import BaseModel, EmailStr, Field

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: str
    profile_img : str | None = None
    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    email: EmailStr = Field(
        examples=['bob@domain.com'],
        description='Email address untuk user.'
    )
    full_name: str = Field(
        examples=['Dewa Krisna']
    )
    username: str = Field(
        examples=['bob']
    )
    password: str = Field(
        examples=['Password#1234'],
        exclude=True
    )


class UserLogin(BaseModel):
    email_or_username: str = Field(
        examples=['bob']
    )
    password: str = Field(
        examples=['Password#1234']
    )

class UserRequest(BaseModel):
    body:UserLogin

class UserInfoGoogle(BaseModel):
    id: int
    email: EmailStr
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: str

class TokenType(str, Enum):
    ACCESS = 'ACCESS'
    REFRESH = 'REFRESH'

class Token(BaseModel):
    access_token: str
    refresh_token: str

class TokenData(BaseModel):
    id: int | None = None
    username: str | None = None

class RefreshInput(BaseModel):
    refresh_token: str

class GoogleToken(BaseModel):
    google_access_token: str