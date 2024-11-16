from sqlmodel import Field, SQLModel,Column
import enum
class LikeCond(enum.Enum):
    like=1
    netral=0
    dislike=-1

class Likes(SQLModel, table=True):
    id: int = Field(primary_key=True, sa_column_kwargs={'autoincrement': True})
    like: LikeCond = Field(
        sa_column=Column(
            enum.Enum(LikeCond),
            default=None,
            nullable=True,
            index=False
        )
    )
    post_id: int | None = Field(default=None, foreign_key="posts.id")
    user_id: int | None = Field(default=None, foreign_key="users.id")