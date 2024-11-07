from abc import ABC, abstractmethod

class IGravitational(ABC):
    @abstractmethod
    def get_weight(self) -> list:
        raise NotImplementedError
    