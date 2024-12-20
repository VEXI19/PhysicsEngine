from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray
from .IObject import IObject


class IThrust(ABC):
    def __init__(self, cot, engine_angle: NDArray[np.float64] = None):
        """ @param cot: Center of Thrust, a distance in z axis from the center of mass of the rocket.
            @param engine_angle: The angle of the engine relative to the local
            frame of the rocket."""
        self._cot = cot
        self.engine_angle = engine_angle

        if not isinstance(self, IObject):
            raise RuntimeError("Object needs to extend IObject to be IThrust")

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
    
    def get_data_header(self):
        headers = "engine_angle_x,engine_angle_y,engine_angle_z"
        next_headers = super().get_data_header() if hasattr(super(), "get_data_header") else ""
        return f"{headers},{next_headers}"

    def get_data(self):
        data = f"{self.engine_angle[0]},{self.engine_angle[1]},{self.engine_angle[2]}"
        next_data = super().get_data() if hasattr(super(), "get_data") else ""
        return f"{data},{next_data}"