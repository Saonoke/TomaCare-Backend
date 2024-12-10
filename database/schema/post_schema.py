from enum import Enum
from pydantic import BaseModel

class PostUserProfile(BaseModel):
    id: int
    full_name: str
    email: str
    username: str
    profile_img: str

class CommentResponse(BaseModel):
    id : int
    user : PostUserProfile
    commentary : str
    timestamp: str

class PostResponse(BaseModel):
    id :int
    title : str
    body : str
    image_id : int | None = None
    comments : list[CommentResponse] |None = None

    class Config:
        from_attributes = True

class PostResponseGet(PostResponse):
    comments : list[CommentResponse] | None = None
    created_at: str
    image_url: str
    user: PostUserProfile
    count_like : int
    count_dislike: int
    liked : bool
    disliked : bool

class PostInput(BaseModel):
    title : str
    body : str

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
