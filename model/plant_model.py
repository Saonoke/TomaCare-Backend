from sqlmodel import SQLModel, Field, Column, VARCHAR, Enum
import enum


class penyakitEnum(enum.Enum):
    SEHAT='Sehat'
    SAKIT='Sakit'

class Plants(SQLModel,table = True):
    id: int = Field(primary_key=True, sa_column_kwargs={'autoincrement': True})
    user_id : int | None = Field(default=None, foreign_key="users.id")
    title : str = Field(sa_column=Column("title", VARCHAR(100)), max_length=100)
    condition : str = Field(sa_column=Column("condition",Enum(penyakitEnum)))