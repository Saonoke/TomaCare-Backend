from abc import abstractmethod
from typing import List, Optional

from model import Posts
from database.schema  import PostInput,PostResponse,ReactionInput

class PostServiceMeta:
    @abstractmethod
    def get_all(self) -> List[Optional[PostResponse]]:
        pass
    @abstractmethod
    def add(self, post: PostInput) -> PostResponse:
        pass

    @abstractmethod
    def get_by_id(self, _id : int) -> PostResponse:
        pass

    @abstractmethod
    def get_by_user_id(self, _user_id : int) -> List[Optional[PostResponse]]:
        pass

    @abstractmethod
    def edit(self, post: PostInput, _id: int) -> PostResponse:
        pass

    @abstractmethod
    def delete(self, _id :int) -> bool:
        pass

    # REACTION
    @abstractmethod
    def reaction(self, _post_id :int, _type: ReactionInput) -> bool:
        pass