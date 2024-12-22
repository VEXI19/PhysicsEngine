from abc import ABC, abstractmethod
from numpy.typing import NDArray
import numpy as np

class IEnvironment(ABC):
    """
    Interface for environment class. It is used to get create custom environment for simulation
    """

    @abstractmethod
    def get_air_density(self, position:NDArray[np.float64] = None) -> float:
        """
        Function to get air density at given position
        Args:
            position (NDArray[np.float64]): position to get air density at

        Returns:
            float: air density at given position
        """

        raise NotImplementedError

    @abstractmethod
    def get_speed_of_sound(self, position:NDArray[np.float64] = None) -> float:
        """
        Function to get speed of sound at given position
        Args:
            position (NDArray[np.float64]): position to get speed of sound at

        Returns:
            float: speed of sound at given position
        """

        raise NotImplementedError

    @abstractmethod
    def get_temperature(self, position:NDArray[np.float64] = None) -> float:
        """
        Function to get temperature at given position
        Args:
            position (NDArray[np.float64]): position to get temperature at

        Returns:
            float: temperature at given position
        """
        raise NotImplementedError

    @abstractmethod
    def get_pressure(self, position: NDArray[np.float64] = None) -> float:
        """
        Function to get pressure at given position
        Args:
            position (NDArray[np.float64]): position to get pressure at

        Returns:
            float: pressure at given position
        """

        raise NotImplementedError

    @abstractmethod
    def get_wind(self, position: NDArray[np.float64] = None) -> NDArray[np.float64]:
        """
        Function to get wind at given position
        Args:
            position (NDArray[np.float64]): position to get wind at

        Returns:
            NDArray[np.float64]: wind at given position
        """

        raise NotImplementedError

    @abstractmethod
    def get_wind_gradient(self, position: NDArray[np.float64] = None) -> NDArray[np.float64]:
        """
        Function to get wind gradient at given position
        Args:
            position (NDArray[np.float64]): position to get wind gradient at

        Returns:
            NDArray[np.float64]: wind gradient at given position
        """

        raise NotImplementedError