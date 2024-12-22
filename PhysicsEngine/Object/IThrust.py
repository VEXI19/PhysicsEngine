from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray
from .IObject import IObject


class IThrust(ABC):
    """
    Interface for thrust objects. It is used to create custom thrust objects for simulation

    Attributes:
        _cot: center of thrust, a distance in local z axis from the center of mass of the object
        _engine_angle: angle of the engine relative to the local frame of reference
    """
    def __init__(self, cot: float, engine_angle: NDArray[np.float64] = None):
        """
        Constructor for IThrust class

        Args:
            cot (float): center of thrust, a distance in local z axis from the center of mass of the object
            engine_angle (NDArray[np.float64]): initial engine angle
        """

        self._cot = cot
        self.engine_angle = engine_angle

        if not isinstance(self, IObject):
            raise RuntimeError("Object needs to extend IObject to be IThrust")

    @property
    def cot(self) -> float:
        """
        Returns center of thrust of the object

        Returns:
            float: center of thrust of the object
        """
        return self._cot

    @property
    def engine_angle(self) -> NDArray[np.float64]:
        """
        Returns angle of the engine relative to the local frame of reference

        Returns:
            NDArray[np.float64]: engine angle
        """
        return self._engine_angle

    @engine_angle.setter
    def engine_angle(self, engine_angle: NDArray[np.float64]) -> None:
        """
        Sets angle of the engine relative to the local frame of reference

        Args:
            engine_angle (NDArray[np.float64]): engine angle
        """

        if engine_angle is None:
            engine_angle = np.array([0, 0, 0], dtype=np.float64)

        self._engine_angle = engine_angle

    @abstractmethod
    def mass_flow_rate(self, time: float) -> float:
        """
        Function returning mass flow rate of the engine at given time

        Args:
            time (float): time at which mass flow rate is calculated

        Returns:
            float: mass flow rate of the engine at given time
        """
        raise NotImplementedError

    @abstractmethod
    def exhaust_velocity(self, time: float) -> float:
        """
        Function returning exhaust velocity of the engine at given time

        Args:
            time (float): time at which exhaust velocity is calculated

        Returns:
            float: exhaust velocity of the engine at given time
        """

        raise NotImplementedError
