from pydantic import BaseModel, EmailStr


class UserUpdate(BaseModel):
    email: EmailStr
    username: str
    full_name: str

    class Config:
        from_attributes = True

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

class UserCreatePassword(BaseModel):
    password: str