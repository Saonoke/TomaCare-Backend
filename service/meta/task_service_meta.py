from abc import abstractmethod
from database.schema import TaskCreate, TaskShow, TaskUpdate, TaskBase

class TaskServiceMeta: 
    @abstractmethod
    def create_task(self, task:TaskCreate)->TaskShow:
        pass

    @abstractmethod
    def get_task_by_plant(self,plant_id:int)->list[TaskShow]:
        pass

    @abstractmethod
    def update_task(self,task_id:int, data:TaskUpdate):
        pass

    @abstractmethod
    def show_task(self, task_id:int)->TaskShow:
        pass

    @abstractmethod 
    def delete_task(self, task_id:int)->TaskShow:
        pass

   




