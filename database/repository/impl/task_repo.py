from sqlmodel import select, Session
from database.repository.meta import TaskRepositoryMeta
from model import Plants
from database.schema import TaskCreate, TaskUpdate
from model.task_model import Task

class TaskRepository(TaskRepositoryMeta):
    
    def __init__(self, session:Session):
        self.session = session

    def create(self, model: TaskCreate) -> Task:
        task = Task(**model.dict())
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
    
    def update(self, model:TaskUpdate, _id:int)->Task:
        task = self.session.get(Task,_id)
       
        if not task:
            return None
        task_data = model.model_dump(exclude_unset=True)
        task.sqlmodel_update(task_data)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
    
    def show(self, _id:int)->Task:
        task = self.session.get(Task,_id)
        if not task :
            return None
        
        return task
    
    def delete(self, _id:int)->Task:
        task = self.session.get(Task,_id)

        if not task:
            return None
        self.session.delete(task)
        self.session.commit()
        return task
    
    def delete_by_plant(self,task:list[Task]):
        for task_item in task:
            self.session.delete(task_item)
            self.session.commit()
        
        return task
            
    
    def getByPlant(self, plant_id:int)->list[Task]:
        plant = self.session.get(Plants,plant_id)

        if not plant:
            return None
        
        return plant.task
    
        
        

