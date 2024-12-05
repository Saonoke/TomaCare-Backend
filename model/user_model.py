from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, VARCHAR, Column, String, Relationship

from model.comment_model import Comments
from model.reaction_model import Reaction

class Users(SQLModel, table=True):
    id: int = Field(primary_key=True, sa_column_kwargs={'autoincrement': True})
    email: EmailStr = Field(sa_column=Column("email", VARCHAR(100), unique=True), max_length=100)
    username: str = Field(sa_column=Column("username", VARCHAR(100), unique=True), max_length=100)
    full_name: str = Field(max_length=200)
    password: str = Column(String(200))
    profile_img: int | None = Field(default=None,foreign_key="images.id")
    posts_links: list[Reaction] = Relationship(back_populates="user")
    posts_comments: list[Comments] = Relationship(back_populates="user")
    posts: list['Posts'] = Relationship(back_populates='user')
    profile: 'Images' = Relationship(back_populates='user')
