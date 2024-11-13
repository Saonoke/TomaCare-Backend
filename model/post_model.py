from sqlmodel import Field, SQLModel, Relationship


class Posts(SQLModel, table=True):
    id: int = Field(primary_key=True, sa_column_kwargs={'autoincrement': True})
    title : str = Field(max_length=40)
    body : str
    user_id: int | None = Field(default=None, foreign_key="users.id")
    image_id: int = Field(default=None,foreign_key="images.id")
  