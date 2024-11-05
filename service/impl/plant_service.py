import requests

from fastapi import Depends, HTTPException
from sqlmodel import Session
from database.repository import PlantRepositoryMeta,PlantRepository
from database.schema import PlantBase,PlantCreate,PlantShow,PlantUpdate
from service import PlantServiceMeta


class PlantService(PlantServiceMeta):
    
    def __init__(self,session:Session) :
        self.session = session
        self._plant_repository : PlantRepositoryMeta = PlantRepository(self.session)
        

    def create_plant(self, data: PlantCreate) -> PlantShow:
        try:
            plant = self._plant_repository.create(data)
        except Exception as e:
            raise e
        return plant
    
    def show_all_plant(self) -> list[PlantShow]:
        try:
            plant = self._plant_repository.getAll()
        except Exception as e:
            raise e
        return plant
    
    def show_plant(self, plant_id: int) -> PlantShow:
        try:
            plant = self._plant_repository.show(plant_id)
            if not plant:
                raise HTTPException(status_code= 404,detail="Item Not Found")
        except Exception as e:
            raise e
        
        return plant
    
    def delete_plant(self, plant_id: int) -> PlantShow:
        try:
            plant = self._plant_repository.delete(plant_id)
            if not plant:
                raise HTTPException(status_code= 404,detail="Item Not Found")
        except Exception as e:
            raise e
        return plant
    
    def update_plant(self, plant_id: int, data: PlantUpdate) -> PlantShow:
        print('tes')
        try:
            plant = self._plant_repository.update(data,plant_id)
            if not plant:
                raise HTTPException(status_code= 404,detail="Item Not Found")
        except Exception as e:
            raise e
        return plant
    


    