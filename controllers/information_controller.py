from typing import List
from sqlmodel import Session
from controllers.base_controller import BaseController
from model import Users
from database.schema import InformationResponse
from service.meta import PostServiceMeta
from service.impl import PostService, InformationService
from service.meta import InformationServiceMeta


class InformationController(BaseController):
    _information_service: InformationServiceMeta

    def __init__(self, session: Session):
        self._information_service: InformationServiceMeta = InformationService(session)

    def get_all(self) -> List[InformationResponse]:
        try:
            informations = self._information_service.get_all()
            return [InformationResponse.model_validate(information) for information in informations]
        except Exception as e:
            return e

    def get_by_id(self, _id: int) -> InformationResponse:
        try:
            return self._information_service.get_by_id(_id)
        except Exception as e:
            return self.ise(e)