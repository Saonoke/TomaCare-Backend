from pydantic import BaseModel
from datetime import date

class TaskBase(BaseModel):
    title: str | None = None
    done: bool | None = False

class TaskCreate(TaskBase):
    plant_id : int 
    id : int | None= None
    tanggal : date 

class TaskShow(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass






