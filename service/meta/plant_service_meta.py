from abc import abstractmethod
from database.schema import PlantCreate, PlantShow, PlantUpdate, PlantBase

class PlantServiceMeta:
    @abstractmethod
    def create_plant(self,plant:PlantCreate)->PlantBase:
        pass
    
    @abstractmethod
    def show_all_plant(self)->list[PlantBase]:
        pass

    @abstractmethod
    def show_plant(self,plant_id:int)->PlantBase:
        pass

    @abstractmethod
    def delete_plant(self,plant_id:int)->PlantBase:
        pass

    @abstractmethod
    def update_plant(self,plant_id:int,data:PlantUpdate)->PlantBase:
        pass


    