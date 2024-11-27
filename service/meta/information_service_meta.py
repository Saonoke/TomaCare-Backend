from abc import abstractmethod
from typing import List, Optional

from database.schema  import PostResponse

class InformationServiceMeta:
    @abstractmethod
    def get_all(self) -> List[Optional[PostResponse]]:
        pass

    @abstractmethod
    def get_by_id(self, _id : int) -> PostResponse:
        pass