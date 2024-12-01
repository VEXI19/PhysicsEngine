from abc import ABC, abstractmethod


class IThrust(ABC):
    @abstractmethod
    def mass_flow_rate(self, time: float) -> float:
        raise NotImplementedError

    @abstractmethod
    def exhaust_velocity(self, time: float) -> float:
        raise NotImplementedError
    
