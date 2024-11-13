from enum import Enum
from pydantic import BaseModel

class PostResponse(BaseModel):
    id :int 
    title : str
    body : str
    user_id : int
    image_id : int | None = None
    
    class Config:
        from_attributes = True

class PostInput(BaseModel):
    title : str
    body : str
    image_path : str
    

class ReactionEnum(str, Enum):
    LIKE = "Like"
    DISLIKE = "Dislike"

class ReactionInput(BaseModel):
    type: ReactionEnum

class ReactionResponse(BaseModel):
    action: str
    success: bool

