from sqlmodel import SQLModel, Field, Column, VARCHAR,Enum,  Relationship
from enumeration import penyakitEnum

from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from model import Task



class Plants(SQLModel,table = True):
    id: int = Field(primary_key=True, sa_column_kwargs={'autoincrement': True})
    user_id : int | None = Field(default=None, foreign_key="users.id")
    title : str = Field(sa_column=Column("title", VARCHAR(100)), max_length=100)
    condition : str = Field(sa_column=Column("condition",Enum(penyakitEnum)))
    image_id: int | None = Field(default=None,foreign_key="images.id")
    task : list["Task"] = Relationship(back_populates="plants", cascade_delete=True)
    created_at : date | None= Field(default_factory=lambda: datetime.now())
    done : bool = Field(default=False)
    image: 'Images' = Relationship(back_populates='plant')

    