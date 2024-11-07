from abc import ABC, abstractmethod

class IObject(ABC):
    @abstractmethod
    def get_position(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def get_rotation(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def get_velocity(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def get_mass(self) -> float:
        raise NotImplementedError