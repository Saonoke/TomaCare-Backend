from typing import List, Optional
from sqlmodel import select, Session

from database.repository.meta import InformationRepositoryMeta
from model import Information


class InformationRepository(InformationRepositoryMeta):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Optional[Information]]:
        statement = select(Information)
        results = self.session.exec(statement).all()
        return results

    def get_by_id(self, _id: int) -> Information:
        result = self.session.get(Information, _id)
        return result
