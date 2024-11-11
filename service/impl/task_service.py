from fastapi import HTTPException
from sqlmodel import Session
from database.repository import TaskRepositoryMeta, TaskRepository
from database.schema import TaskBase, TaskCreate, TaskShow, TaskUpdate
from service import TaskServiceMeta

class TaskService(TaskServiceMeta):
    def __init__(self,session:Session) :
        self.session = session
        self._task_repository : TaskRepositoryMeta = TaskRepository(self.session)

    def create_task(self, data: TaskCreate) -> TaskShow:
        # id plant
        try:
            task = self._task_repository.create(data)
        except Exception as e:
            raise e
        return task
    
    def get_task_by_plant(self,plant_id:int)->list[TaskShow]:
        # rombak 
        try:
            task = self._task_repository.getByPlant(plant_id)
            if not task:
                raise HTTPException(status_code= 404,detail="Task Not Found")
        except Exception as e:
            raise e
        return task
    
    def show_task(self, task_id: int) -> TaskShow:
        try:
            task = self._task_repository.show(task_id)
            if not task:
                raise HTTPException(status_code= 404,detail="Task Not Found")
        except Exception as e:
            raise e 
        return task
    
    def update_task(self,  data: TaskUpdate,task_id: int):
        try:
            print(data)
            task = self._task_repository.update(data,task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
        except Exception as e:
            raise e
        return task
    
    def delete_task(self, task_id: int) -> TaskShow:
        try:
            task = self._task_repository.delete(task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
        except Exception as e:
            raise e
        return task
    
  



    
        