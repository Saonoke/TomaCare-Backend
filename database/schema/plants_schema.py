from pydantic import BaseModel, Field
from database.schema.image_schema import ImageResponse

class PlantBase(BaseModel):
    title: str | None = None
    condition: str | None =None

class PlantCreate(PlantBase):
    image_path : str
    
class PlantShow(PlantBase):
    id:int
    image:ImageResponse

class PlantUpdate(PlantBase):
    pass


    
