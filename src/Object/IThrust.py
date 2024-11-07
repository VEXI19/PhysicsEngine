from abc import ABC, abstractmethod

class IThrust(ABC):
    @abstractmethod
    def get_thrust(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_mass_flow_rate(self, time=None) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_exhaust_velocity(self, time=None) -> float:
        raise NotImplementedError
    
