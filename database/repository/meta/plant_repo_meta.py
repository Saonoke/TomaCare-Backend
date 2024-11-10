from abc import abstractmethod
from sqlmodel import Session
from model import Plants

class PlantRepositoryMeta:
    @abstractmethod
    def create(self,model:Plants) -> Plants:
        pass

    @abstractmethod
    def update(self,model:Plants,_id:int) -> Plants:
        pass
    
    @abstractmethod
    def show(self,_id:int) -> Plants:
        pass

    @abstractmethod
    def delete(self,_id:int) -> Plants:
        pass

    def getAll(self, _user_id:int) -> list[Plants]:
        pass


    