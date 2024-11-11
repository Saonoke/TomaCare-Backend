from abc import abstractmethod
from model import Task

class TaskRepositoryMeta:

    @abstractmethod
    def create(self, model : Task)->Task:
        pass

    @abstractmethod
    def update(self, model:Task, _id:int)->Task:
        pass

    @abstractmethod
    def show(self, _id:int)->Task:
        pass

    @abstractmethod
    def delete(self, _id:int)->Task:
        pass

    @abstractmethod
    def getByPlant(self, plant_id:int)->Task:
        pass

    @abstractmethod
    def delete_by_plant(task:list[Task]):
        pass
    