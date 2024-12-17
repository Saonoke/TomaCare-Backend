import requests

from fastapi import Depends, HTTPException
from sqlmodel import Session
from database.repository import PlantRepositoryMeta,PlantRepository,ImageRepositoryMeta,ImageRepository
from database.schema import PlantBase,PlantCreate,PlantShow,PlantUpdate
from model import Users,Images,Plants
from service import PlantServiceMeta, TaskServiceMeta
from .task_service import TaskService
from enumeration import penyakitEnum


class PlantService(PlantServiceMeta):
    
    def __init__(self, user: Users, session:Session) :
        self.session = session
        self._plant_repository : PlantRepositoryMeta = PlantRepository(self.session)
        self._user: Users = user
        self._image_repository :ImageRepositoryMeta = ImageRepository(self.session)
        self._task_service: TaskServiceMeta = TaskService(user,session)
        

    def create_plant(self, data: PlantCreate) :
        try:
            user_id = self._user.id
            image = Images(image_path=data.image_path)
            image_id = self._image_repository.create(image)
            condition = penyakitEnum.get_enum_by_value(data.condition)
            print(condition)
            if(condition == None):
                raise HTTPException(status_code=400 ,detail="Create Failed, Penyakit tidak ditemukan")
            plant = Plants(title=data.title,condition=condition,user_id=user_id,image_id=image_id)
            plant = self._plant_repository.create(plant)
            task = self._task_service.create_task(condition,plant.id)
            print(task)
            self.session.commit()
            return plant
        except Exception as e:
            print(e)
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Create Failed")
        
    
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
            if not plant:
                    raise HTTPException(status_code= 404,detail="Item Not Found")
            if plant and (plant.user_id != self._user.id):
                raise HTTPException(status_code=403, detail="Forbidden: You do not have access to this plant")
            try :
                self._image_repository.delete(plant.image_id)
                plant = self._plant_repository.delete(plant_id)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise e
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
    


    