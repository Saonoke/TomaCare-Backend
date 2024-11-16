from abc import abstractmethod
from typing import List

from model import Images

class ImageRepositoryMeta :
    @abstractmethod
    def get_all(self) ->List[Images] :
        pass
    @abstractmethod
    def get_by_id(self, _id : int) -> Images :
        pass

    @abstractmethod
    def create(self, image : Images) -> int :
        pass

    @abstractmethod
    def edit(self, image : Images,_id : int) -> bool :
        pass


    @abstractmethod
    def delete(self, _id: int) -> bool  :
        pass


