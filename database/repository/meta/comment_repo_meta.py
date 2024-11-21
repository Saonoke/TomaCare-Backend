from abc import abstractmethod
from typing import Optional

from model import Comments

class CommentRepositoryMeta:
    def get(self, _post_id: int, _comment_id: int) -> Optional[Comments]:
        pass

    @abstractmethod
    def add(self, model: Comments):
        pass

    @abstractmethod
    def edit(self, model: Comments):
        pass

    @abstractmethod
    def delete(self, _post_id: int,_comment_id : int):
        pass
