from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.repository import ImageRepository,ImageRepositoryMeta
from database.schema import ImageBase,ImageResponse
from service.meta import ImageServiceMeta
from model import Images


class ImageService(ImageServiceMeta):

    def __init__(self, session:Session):
        self.session = session
        self._image_repository : ImageRepositoryMeta = ImageRepository(self.session)

    def get_all(self) -> List[Optional[ImageResponse]]:
        return self._image_repository.get_all()
        
    def get_by_id(self,_id : int) -> ImageResponse:
        if not self._image_repository.get_by_id(_id):
            raise HTTPException(status_code=404, detail="ID not found")
        else :
            return self._image_repository.get_by_id(_id)
    
    def create(self, image: ImageBase) -> int:
        return self._image_repository.create(image)

    def delete(self, _id:int) -> bool:
        if not self._image_repository.get_by_id(_id):
            raise HTTPException(status_code=404, detail="ID not found")
        else :
            return self._image_repository.delete(_id)

