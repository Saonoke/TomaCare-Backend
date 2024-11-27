from sqlmodel import Field, SQLModel, Column, Text

class Information(SQLModel, table=True):
    id: int = Field(primary_key=True, sa_column_kwargs={'autoincrement': True})
    title: str = Field(max_length=255)
    content: str = Field(sa_column=Column('content', Text()))
    medicine: str = Field(sa_column=Column('medicine', Text()))

