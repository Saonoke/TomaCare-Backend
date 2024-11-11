from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str | None = None
    done: bool | None = False

class TaskCreate(TaskBase):
    plant_id : int 
    id : int | None= None

class TaskShow(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass






