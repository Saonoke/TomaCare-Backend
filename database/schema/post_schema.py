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

class PostResponseGet(PostResponse):
    count_like : int
    count_dislike: int
    liked : bool
    disliked : bool

class PostInput(BaseModel):
    title : str
    body : str
    image_id : int

class ReactionEnum(str, Enum):
    LIKE = "Like"
    DISLIKE = "Dislike"

class ReactionInput(BaseModel):
    type: ReactionEnum

class ReactionResponse(BaseModel):
    action: str
    success: bool