from sqlmodel import SQLModel, Field, Column, Enum, Relationship
import enum

class ReactionEnum(enum.Enum):
    LIKE='Like'
    DISLIKE='Dislike'

class Reaction(SQLModel, table=True):
    posts_id: int = Field(foreign_key="posts.id", primary_key=True)
    users_id: int = Field(foreign_key="users.id", primary_key=True)

    reaction_type: str = Field(sa_column=Column(Enum(ReactionEnum), nullable=False))

    user: "Users" = Relationship(back_populates="posts_links")
    post: "Posts" = Relationship(back_populates="users_links")