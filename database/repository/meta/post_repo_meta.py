from abc import abstractmethod
from typing import List, Optional

from model import Posts     

class PostRepositoryMeta:
    @abstractmethod
    def get_all(self, search: Optional[str], limit: int) ->List[Posts] :
        pass

    @abstractmethod
    def add(self, model: Posts  ) -> Posts   :
        pass

    @abstractmethod
    def edit(self, model: Posts, _id: int) -> Posts    :
        pass

    @abstractmethod
    def get_by_id(self, _id: int) -> Posts  :
        pass

    @abstractmethod
    def get_by_user_id(self, _user_id: int) -> List[Posts]    :
        pass

    @abstractmethod
    def delete(self, _id: int) -> bool  :
        pass