from datetime import date
from pydantic import BaseModel, Field
from database.schema.image_schema import ImageResponse

class PlantBase(BaseModel):
    title: str | None = None
    condition: str | None =None
    done: bool | None = None
    created_at: date

class PlantCreate(PlantBase):
    image_path : str
    
class PlantShow(PlantBase):
    id:int
    image:ImageResponse

class PlantUpdate(BaseModel):
    title: str
