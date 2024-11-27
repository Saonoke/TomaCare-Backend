from typing import List, Optional
from sqlmodel import Session

from database.repository.impl.information_repo import InformationRepository
from database.repository.meta import InformationRepositoryMeta
from database.schema import InformationResponse
from service.meta.information_service_meta import InformationServiceMeta
from model import Information


class InformationService(InformationServiceMeta):
    def __init__(self, session: Session):
        self._post_repository: InformationRepositoryMeta = InformationRepository(session)

    def get_all(self) -> List[Optional[InformationResponse]]:
        posts = self._post_repository.get_all()
        responses = []
        for post in posts:
            responses.append(
                InformationResponse(**post.model_dump())
            )
        return responses

    def get_by_id(self, _id: int) -> Information:
        return self._post_repository.get_by_id(_id)