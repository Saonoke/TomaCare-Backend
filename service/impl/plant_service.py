import requests

from fastapi import Depends, HTTPException
from sqlmodel import Session
from database.repository import PlantRepositoryMeta,PlantRepository
from database.schema import PlantBase,PlantCreate,PlantShow,PlantUpdate
from model import Users
from service import PlantServiceMeta


class PlantService(PlantServiceMeta):
    
    def __init__(self, user: Users, session:Session) :
        self.session = session
        self._plant_repository : PlantRepositoryMeta = PlantRepository(self.session)
        self._user: Users = user
        

    def create_plant(self, data: PlantCreate) -> PlantShow:
        try:
            data.user_id = self._user.id
            plant = self._plant_repository.create(data)
        except Exception as e:
            raise e
        return plant
    
    def show_all_plant(self) -> list[PlantShow]:
        try:
            plant = self._plant_repository.getAll(self._user.id)
        except Exception as e:
            raise e
        return plant
    
    def show_plant(self, plant_id: int) -> PlantShow:
        try:
            plant = self._plant_repository.show(plant_id)
            if not plant:
                raise HTTPException(status_code= 404,detail="Item Not Found")
            if plant.user_id != self._user.id:
                raise HTTPException(status_code= 403, detail="Forbidden: You do not have access to this plant")
        except Exception as e:
            raise e
        
        return plant
    
    def delete_plant(self, plant_id: int) -> PlantShow:
        try:
            plant = self._plant_repository.show(plant_id)
            if plant and (plant.user_id != self._user.id):
                raise HTTPException(status_code=403, detail="Forbidden: You do not have access to this plant")
            plant = self._plant_repository.delete(plant_id)
            if not plant:
                raise HTTPException(status_code= 404,detail="Item Not Found")
        except Exception as e:
            raise e
        return plant
    
    def update_plant(self, plant_id: int, data: PlantUpdate) -> PlantShow:
        try:
            plant = self._plant_repository.show(plant_id)
            if plant and (plant.user_id != self._user.id):
                raise HTTPException(status_code= 403, detail="Forbidden: You do not have access to this plant")
            plant = self._plant_repository.update(data, plant_id)
            if not plant:
                raise HTTPException(status_code= 404,detail="Item Not Found")
        except Exception as e:
            raise e
        return plant
    


    