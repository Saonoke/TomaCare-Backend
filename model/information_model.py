from sqlmodel import Field, SQLModel, Column, Text, Enum
import enum
from enumeration import informationEnum

class Information(SQLModel, table=True):
    id: int = Field(primary_key=True, sa_column_kwargs={'autoincrement': True})
    type: str = Field(sa_column=Column("type",Enum(informationEnum)))
    title: str = Field(max_length=255)
    content: str = Field(sa_column=Column('content', Text()))
    medicine: str = Field(sa_column=Column('medicine', Text()))


