from abc import ABC
from ..Types import Vector3
import numpy as np
from numpy.typing import NDArray


class IObject(ABC):
    def __init__(self, position: NDArray[np.float64] = None, rotation: NDArray[np.float64] = None, velocity: NDArray[np.float64] = None, acceleration: NDArray[np.float64] = None):
        self.position = position
        self.rotation = rotation
        self.velocity = velocity
        self.acceleration = acceleration

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: NDArray[np.float64]):
        if position is None:
            position = np.array([0, 0, 0], dtype=np.float64)

        self._position = position

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: NDArray[np.float64]):
        if rotation is None:
            rotation = np.array([0, 0, 0], dtype=np.float64)

        self._rotation = rotation

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, acceleration: NDArray[np.float64]):
        if acceleration is None:
            acceleration = np.array([0, 0, 0], dtype=np.float64)

        self._acceleration = acceleration

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: NDArray[np.float64]):
        if velocity is None:
            velocity = np.array([0, 0, 0], dtype=np.float64)

        self._velocity = velocity

    def update(self, position: NDArray[np.float64] = None, rotation: NDArray[np.float64] = None, velocity: NDArray[np.float64] = None):
        if position is not None:
            self.position = position

        if rotation is not None:
            self.rotation = rotation

        if velocity is not None:
            self.velocity = velocity

    def get_data(self):
        return f"{self.position[0]},{self.position[1]},{self.position[2]},{self.rotation[0]},{self.rotation[1]},{self.rotation[2]},{self.velocity[0]},{self.velocity[1]},{self.velocity[2]},{self.acceleration[0]},{self.acceleration[1]},{self.acceleration[2]},12"

    def __str__(self):
        return f"Position: {self.position}, Rotation: {self.rotation}, Velocity: {self.velocity}, Acceleration: {self.acceleration}"
