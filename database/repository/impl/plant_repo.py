from sqlmodel import select, Session
from database.repository.meta import PlantRepositoryMeta
from model import Plants
from database.schema import PlantCreate, PlantUpdate


class PlantRepository(PlantRepositoryMeta):

    def __init__(self,session:Session):
        self.session = session

    def create(self, model: Plants) -> Plants:
        self.session.add(model)
        self.session._flush()
        return model
        
    def update(self,model: PlantUpdate,_id:int) -> Plants:
        plant = self.session.get(Plants,_id)
        if not plant:
            return None    
        plant_data = model.model_dump(exclude_unset=True)
        plant.sqlmodel_update(plant_data)
        self.session.add(plant)
        self.session.flush()
        return plant
    
            
    def show(self,_id:int):
        plant = self.session.get(Plants,_id)
        if not plant:
            return None
        
        return plant

    def delete(self,_id:int):
        plant = self.session.get(Plants,_id)
        if not plant:
            return None
        self.session.delete(plant)
        self.session.commit()
        return plant

    
    def getAll(self, _user_id: int):
       plants = self.session.exec(select(Plants).where(Plants.user_id == _user_id)).all()
       if not plants:
           return []
       return plants
    
    
    

    
    
        

       

        

    

        

        

     
