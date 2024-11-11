from sqlmodel import SQLModel, Field, Relationship

from typing import TYPE_CHECKING,Optional

if TYPE_CHECKING:
    from model import Plants

class Task(SQLModel,table = True):
    id: int = Field(primary_key=True)
    plant_id : int = Field(default=None, foreign_key="plants.id")
    title : str = Field(max_length=40)
    done : bool = Field(default=False)
    plants : Optional["Plants"] | None = Relationship(back_populates="task")