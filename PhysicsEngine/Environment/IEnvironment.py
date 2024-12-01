from abc import ABC, abstractmethod

class IEnvironment(ABC):
    @abstractmethod
    def get_air_density(self, position=None) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_speed_of_sound(self, position=None) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_temperature(self, position=None) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_pressure(self, position=None) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_wind(self, position=None) -> list:
        raise NotImplementedError

    @abstractmethod
    def get_wind_gradient(self, position=None) -> list:
        raise NotImplementedError