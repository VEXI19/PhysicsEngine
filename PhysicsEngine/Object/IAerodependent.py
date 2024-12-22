from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray
from .IObject import IObject
from ..Utils.Constants import Constants as C


class IAerodependent(ABC):
    """
    Interface for aerodependent objects. It is used to create custom aerodependent objects for simulation

    Attributes:
        _cop: center of pressure
        _angle_of_attack: angle of attack
        _relative_velocity: relative velocity
        _reference_area: reference area
        _drag_coefficient: drag coefficient
    """
    def __init__(self, cop: float, angle_of_attack: NDArray[np.float64] = None, relative_velocity: NDArray[np.float64] =
    None, drag_coefficient: float = C.DRAG_COEFFICIENT_PARALLEL.value):
        """
        Constructor for IAerodependent class

        Args:
            cop (float): center of pressure
            angle_of_attack (NDArray[np.float64]): initial angle of attack
            relative_velocity (NDArray[np.float64]): initial relative velocity
            drag_coefficient (float): drag coefficient
        """
        self._cop = cop
        self.angle_of_attack = angle_of_attack
        self.relative_velocity = relative_velocity
        self._reference_area = self.calculate_reference_area()
        self.drag_coefficient = drag_coefficient

        if not isinstance(self, IObject):
            raise RuntimeError("Object needs to extend IObject to be IAerodependent")

    @property
    def reference_area(self) -> float:
        """
        Returns reference area of the object

        Returns:
            float: reference area of the object
        """

        return self._reference_area
            
    @property
    def cop(self) -> float:
        """
        Returns center of pressure of the object

        Returns:
            float: center of pressure of the object
        """

        return self._cop

    @property
    def angle_of_attack(self) -> NDArray[np.float64]:
        """
        Returns angle of attack of the object

        Returns:
            NDArray[np.float64]: angle of attack of the object
        """
        return self._angle_of_attack

    @angle_of_attack.setter
    def angle_of_attack(self, angle_of_attack: NDArray[np.float64]) -> None:
        """
        Sets angle of attack of the object

        Args:
            angle_of_attack (NDArray[np.float64]): angle of attack
        """
        if angle_of_attack is None:
            angle_of_attack = [0, 0, 0]

        self._angle_of_attack = angle_of_attack

    @property
    def relative_velocity(self) -> NDArray[np.float64]:
        """
        Returns relative velocity of the object

        Returns:
            NDArray[np.float64]: relative velocity of the object
        """
        return self._relative_velocity

    @relative_velocity.setter
    def relative_velocity(self, relative_velocity: NDArray[np.float64]) -> None:
        """
        Sets relative velocity of the object

        Args:
            relative_velocity (NDArray[np.float64]): relative velocity of the object
        """
        if relative_velocity is None:
            relative_velocity = [0, 0, 0]

        self._relative_velocity = relative_velocity

    @property
    def drag_coefficient(self) -> float:
        """
        Returns drag coefficient of the object

        Returns:
            float: drag coefficient of the object
        """
        return self._drag_coefficient

    @drag_coefficient.setter
    def drag_coefficient(self, drag_coefficient: float) -> None:
        """
        Sets drag coefficient of the object

        Args:
            drag_coefficient (float): drag coefficient of the object
        """

        self._drag_coefficient = drag_coefficient

    def calculate_reference_area(self: IObject) -> float:
        """
        Function to calculate reference area

        Returns:
            float: reference area
        """

        reference_area = 0

        for face in self.object_model.faces:
            vertices = self.object_model.vertices[face]

            projected_vertices = vertices[:, :2]

            x = projected_vertices[:, 0]
            y = projected_vertices[:, 1]

            area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

            reference_area += area

        return reference_area
