from pydantic import EmailStr
from sqlmodel import Field, SQLModel, VARCHAR, Column, String, Relationship

class Users(SQLModel, table=True):
    id: int = Field(primary_key=True, sa_column_kwargs={'autoincrement': True})
    email: EmailStr = Field(sa_column=Column("email", VARCHAR(100), unique=True), max_length=100)
    username: str = Field(sa_column=Column("username", VARCHAR(100), unique=True), max_length=100)
    full_name: str = Field(max_length=200)
    password: str = Column(String(200))

