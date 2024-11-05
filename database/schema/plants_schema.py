from pydantic import BaseModel, Field

class PlantBase(BaseModel):
    title: str | None = None
    condition: str | None =None

class PlantCreate(PlantBase):
    user_id: int
    
class PlantShow(PlantBase):
    id:int

class PlantUpdate(PlantBase):
    pass


    
