from fastapi import Depends, HTTPException
from database.database import get_session
from sqlmodel import Session
from database.schema import PlantBase, PlantCreate, PlantUpdate, PlantShow
from service import PlantService, PlantServiceMeta
from controllers.base_controller import BaseController

class PlantController(BaseController):
    
    def __init__(self,session:Session):
        self._plant_service : PlantServiceMeta = PlantService(session)
    
    def create_plant (self,data:PlantCreate) -> PlantCreate:
        try:
            return self._plant_service.create_plant(data)
        except Exception as e:
            raise self.ise(e)
    
    def get_all_plan(self)->list[PlantShow]:
        try:
            
            plan =self._plant_service.show_all_plant()
            return plan
        except Exception as e:
            raise self.ise(e)
        
    
    def show_plan_with_task(self,plant_id:int)->PlantShow:
        try:
            # get with task
            return self._plant_service.show_plant(plant_id)
        except Exception as e:
            raise self.ise(e)
        
    def delete_plan(self,plant_id:int)->PlantBase:
        try:
            # delete task 
            return self._plant_service.delete_plant(plant_id)
        except Exception as e:
            raise self.ise(e)
        
    def update_plan(self,plant_id:int, data:PlantUpdate)->PlantBase:
        try:
            return self._plant_service.update_plant(plant_id,data)
        except Exception as e:
            raise self.ise(e)
        
        
    
        
    

