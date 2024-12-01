from abc import ABC, abstractmethod


class IAerodependent(ABC):
    @abstractmethod
    def reference_area(self, alpha: float = None) -> float:
        raise NotImplementedError

    @abstractmethod
    def drag_coefficient(self, alpha: float = None) -> float:
        raise NotImplementedError
