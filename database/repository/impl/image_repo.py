from typing import List, Optional
from sqlmodel import select, Session

from database.repository.meta import ImageRepositoryMeta
from model import Images
from database.database import engine

class ImageRepository(ImageRepositoryMeta):
    def __init__(self,session:Session):
        self.session = session
        
    def get_all(self) -> List[Optional[Images]]:
        statement = select(Images)
        results = self.session.exec(statement).all()
        return results
    def get_by_id(self, _id: int) -> Images:
        result = self.session.get(Images, _id)
        return result
    
    def create(self, model: Images) -> int:
        self.session.add(model)
        self.session.flush()
        return model.id
    
    def edit(self, _id : int,model: Images,) -> bool:
        statement = select(Images).where(Images.id == _id)
        results = self.session.exec(statement)
        db_image = results.one()
        if db_image is None:
            return None
        db_image.image_path = model.image_path
        self.session.add(db_image)
        self.session.flush()
        return db_image
    
    def delete(self, _id: int) -> bool  :
        statement = select(Images).where(Images.id == _id)
        results = self.session.exec(statement)
        db_images = results.one()
        if db_images is None:
            return None
        self.session.delete(db_images)
        self.session.commit()
        return True

    
