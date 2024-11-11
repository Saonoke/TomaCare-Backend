from abc import abstractmethod
from database.schema import PlantCreate, PlantShow, PlantUpdate

class PlantServiceMeta:
    @abstractmethod
    def create_plant(self,plant:PlantCreate)->PlantShow:
        pass
    
    @abstractmethod
    def show_all_plant(self)->list[PlantShow]:
        pass

    @abstractmethod
    def show_plant(self,plant_id:int)->PlantShow:
        pass

    @abstractmethod
    def delete_plant(self,plant_id:int)->PlantShow:
        pass

    @abstractmethod
    def update_plant(self,plant_id:int,data:PlantUpdate)->PlantShow:
        pass


    