from pydantic import BaseModel, EmailStr

from database.schema import UserResponse


class UserResponseProfile(UserResponse):
    hasPassword: bool

class UserUpdate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    profile_img: str

    class Config:
        from_attributes = True

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

class UserCreatePassword(BaseModel):
    password: str