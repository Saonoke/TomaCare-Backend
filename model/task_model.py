from sqlmodel import SQLModel, Field, Column, VARCHAR


class Task(SQLModel,table = True):
    id: int = Field(primary_key=True)
    plant_id : int = Field(default=None, foreign_key="plants.id")
    title : str = Field(max_length=40)
    done : bool = Field(default=False)