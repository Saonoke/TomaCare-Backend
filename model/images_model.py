from sqlmodel import Field, SQLModel, VARCHAR, Column, String

class Images(SQLModel, table=True):
    id: int = Field(primary_key=True, sa_column_kwargs={'autoincrement': True})
    image_path: str 