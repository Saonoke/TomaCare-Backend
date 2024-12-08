from fastapi import UploadFile
from abc import abstractmethod


class MachinelearningMeta:
    @abstractmethod
    def machine_learning_process(self, content ):
        pass
    def check_dauntomat(self, image ) -> bool:
        pass
    