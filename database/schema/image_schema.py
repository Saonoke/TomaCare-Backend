from pydantic import BaseModel

class ImageBase(BaseModel):
    image_path : str

class ImageResponse(ImageBase):
    id:int


    
