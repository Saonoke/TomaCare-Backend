from abc import abstractmethod
from typing import Optional

from model import Reaction

class ReactionRepositoryMeta:
    def get(self, _post_id: int, _user_id: int) -> Optional[Reaction]:
        pass

    @abstractmethod
    def add(self, model: Reaction):
        pass

    @abstractmethod
    def edit(self, model: Reaction):
        pass

    @abstractmethod
    def delete(self, _post_id: int, _user_id: int):
        pass
