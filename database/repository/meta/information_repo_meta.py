from abc import abstractmethod
from model import Information


class InformationRepositoryMeta:

    @abstractmethod
    def get_all(self) -> list[Information]:
        pass

    @abstractmethod
    def get_by_id(self, _id: int) -> Information:
        pass
