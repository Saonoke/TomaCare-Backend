from pydantic import BaseModel, EmailStr, Field

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: str

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

class UserInfoGoogle(BaseModel):
    id: int
    email: EmailStr
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None
    username: str | None = None