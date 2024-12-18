from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray


class IThrust(ABC):

    def __init__(self, cot, engine_angle: NDArray[np.float64] = None):
        """ @param cot: Center of Thrust, a distance in z axis from the center of mass of the object."""
        self._cot = cot
        self.engine_angle = engine_angle

    @property
    def cot(self):
        return self._cot

    @property
    def engine_angle(self):
        return self._engine_angle

    @engine_angle.setter
    def engine_angle(self, engine_angle: NDArray[np.float64]):
        if engine_angle is None:
            engine_angle = np.array([0, 0, 0], dtype=np.float64)

        self._engine_angle = engine_angle

    @abstractmethod
    def mass_flow_rate(self, time: float) -> float:
        raise NotImplementedError

    @abstractmethod
    def exhaust_velocity(self, time: float) -> float:
        raise NotImplementedError
    
