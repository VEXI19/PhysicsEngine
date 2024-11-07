from abc import ABC, abstractmethod

class ICube(ABC):
    @abstractmethod
    def get_length(self) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def get_width(self) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def get_height(self) -> float:
        raise NotImplementedError