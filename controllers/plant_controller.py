from fastapi import Depends, HTTPException
from database.database import get_session
from sqlmodel import Session
from database.schema import PlantBase, PlantCreate, PlantUpdate, PlantShow, TaskUpdate, TaskCreate, TaskShow
from model import Users
from service import PlantService, PlantServiceMeta, TaskServiceMeta, TaskService

from controllers.base_controller import BaseController

class PlantController(BaseController):
    
    def __init__(self, user: Users, session:Session):
        self._plant_service : PlantServiceMeta = PlantService(user, session)
        self._task_service : TaskServiceMeta = TaskService(session)

    def create_plant (self,data:PlantCreate) -> PlantCreate:
        try:
            return self._plant_service.create_plant(data)
        except Exception as e:
            raise self.ise(e)
    
    def create_task (self, data:TaskCreate)-> TaskShow:
        try:
            return self._task_service.create_task(data)
        except Exception as e:
            raise self.ise(e)
    
    def get_all_plan(self)->list[PlantShow]:
        try:
            plan =self._plant_service.show_all_plant()
        except Exception as e:
            raise self.ise(e)
        return plan
        
    def show_plan_with_task(self,plant_id:int)->PlantShow:
        try:
            # gabungkan di service layer
            plant = self._plant_service.show_plant(plant_id)

        except Exception as e:
            raise self.ise(e)
        return {"plant" : plant , "task" : plant.task}
        
    def delete_plan(self,plant_id:int)->PlantBase:
        try:
            return self._plant_service.delete_plant(plant_id)
        except Exception as e:
            raise self.ise(e)
        
    def update_plan(self,plant_id:int, data:PlantUpdate)->PlantBase:
        try:
            return self._plant_service.update_plant(plant_id,data)
        except Exception as e:
            raise self.ise(e)
        
    def update_task(self,task_id:int, data:TaskUpdate):
        try:
            return self._task_service.update_task(data,task_id)
        except Exception as e:
            raise self.ise(e)
        
    def delete_task(self,task_id:int):
        try:
            return self._task_service.delete_task(task_id)
        except Exception as e:
            raise self.ise(e)
    
        
    
        
    

