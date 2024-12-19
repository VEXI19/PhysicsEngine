from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray
from .IObject import IObject


class IAerodependent(ABC):
    def __init__(self, cop, angle_of_attack: NDArray[np.float64] = None, relative_velocity: NDArray[np.float64] = None):
        """ @param cop: Center of Pressure, a distance in z axis from the center of mass of the rocket.
            @param angle_of_attack: The angle between the rocket and the airflow.
            @param relative_velocity: The relative velocity of the rocket and the airflow."""
        self._cop = cop
        self.angle_of_attack = angle_of_attack
        self.relative_velocity = relative_velocity
        self._reference_area = self.calculate_reference_area()

        if not isinstance(self, IObject):
            raise RuntimeError("Object needs to extend IObject to be IAerodependent")

    @property
    def reference_area(self):
        return self._reference_area
            
    @property
    def cop(self):
        return self._cop

    @property
    def angle_of_attack(self):
        return self._angle_of_attack

    @angle_of_attack.setter
    def angle_of_attack(self, angle_of_attack: NDArray[np.float64]):
        if angle_of_attack is None:
            angle_of_attack = [0, 0, 0]

        self._angle_of_attack = angle_of_attack

    @property
    def relative_velocity(self):
        return self._relative_velocity

    @relative_velocity.setter
    def relative_velocity(self, relative_velocity: NDArray[np.float64]):
        if relative_velocity is None:
            relative_velocity = [0, 0, 0]

        self._relative_velocity = relative_velocity

    @abstractmethod
    def reference_area(self, alpha: float = None) -> float:
        raise NotImplementedError


    @abstractmethod
    def drag_coefficient(self, alpha: float = None) -> float:
        raise NotImplementedError

    def calculate_reference_area(self: IObject):
        reference_area = 0

        for face in self.object_model.faces:
            vertices = self.object_model.vertices[face]

            projected_vertices = vertices[:, :2]

            x = projected_vertices[:, 0]
            y = projected_vertices[:, 1]

            area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

            reference_area += area

        return reference_area