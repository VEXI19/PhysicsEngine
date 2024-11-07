from abc import ABC, abstractmethod

class IAerodependent(ABC):
    @abstractmethod
    def get_drag_coefficient(self) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def get_reference_area(self) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def get_lift_coefficient(self) -> float:
        raise NotImplementedError