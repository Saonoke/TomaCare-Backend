from sqlmodel import select, Session, join
from database.repository.meta import PlantRepositoryMeta
from model import Plants, Images
from database.schema import PlantCreate, PlantUpdate, PlantShow, ImageResponse
from sqlalchemy.orm import joinedload


class PlantRepository(PlantRepositoryMeta):

    def __init__(self,session:Session):
        self.session = session

    def create(self, model: Plants) -> Plants:
        self.session.add(model)
        self.session.flush()
        return model
        p
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
       plants = self.session.exec(select(Plants, Images).join(Images).where(Plants.user_id == _user_id)).all()
       if not plants:
           return []
       plants_with_images = []
       for plant,image in plants:
        plants_with_images.append(
                       PlantShow(
               id= plant.id,
               title=plant.title,
               condition=plant.condition,
               image= ImageResponse(
                   id=image.id,
                   image_path= image.image_path
               )
           )
        )
       
       return plants_with_images
    
    
    

    
    
        

       

        

    

        

        

     
