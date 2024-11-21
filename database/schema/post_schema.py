from enum import Enum
from pydantic import BaseModel

class CommentResponse(BaseModel):
    id : int
    user_id : int
    commentary : str

class PostResponse(BaseModel):
    id :int 
    title : str
    body : str
    # user_id : int
    image_id : int | None = None
    comments : list[CommentResponse]

    class Config:
        from_attributes = True

class PostUserProfile(BaseModel):
    id: int
    full_name: str
    profile_img: str

class PostResponseGet(PostResponse):
    image_url: str
    user: PostUserProfile
    count_like : int
    count_dislike: int
    liked : bool
    disliked : bool

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

class CommentInput(BaseModel):
    commentary : str


