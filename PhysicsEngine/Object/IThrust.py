from abc import ABC, abstractmethod


class IThrust(ABC):

    def __init__(self, cot):
        """ @param cot: Center of Thrust, a distance in z axis from the center of mass of the object."""
        self._cot = cot

    @property
    def cot(self):
        return self._cot

    @abstractmethod
    def mass_flow_rate(self, time: float) -> float:
        raise NotImplementedError

    @abstractmethod
    def exhaust_velocity(self, time: float) -> float:
        raise NotImplementedError
    
