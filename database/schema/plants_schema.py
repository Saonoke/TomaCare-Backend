from pydantic import BaseModel, Field

class PlantBase(BaseModel):
    title: str | None = None
    condition: str | None =None

class PlantCreate(PlantBase):
    user_id: int
    image_path : str
    
class PlantShow(PlantBase):
    id:int
    image_id : int

class PlantUpdate(PlantBase):
    pass


    
