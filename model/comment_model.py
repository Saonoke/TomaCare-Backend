from sqlmodel import Field, Relationship, SQLModel
import datetime
from datetime import datetime

class Comments(SQLModel, table=True):
    id: int = Field(primary_key=True, sa_column_kwargs={'autoincrement': True})

    commentary : str
    post_id: int | None = Field(default=None, foreign_key="posts.id",ondelete="CASCADE")
    user_id: int | None = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now())

    user: "Users" = Relationship(back_populates="posts_comments")
    post: "Posts" = Relationship(back_populates="users_comments")