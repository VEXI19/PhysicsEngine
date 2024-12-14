from abc import ABC
from ..Types import Vector3
import numpy as np
from numpy.typing import NDArray


class IObject(ABC):
    def __init__(self, mass: float = 1, length: float = 1,
                 radius: float = 0.1,  position: NDArray[np.float64] = None, rotation: NDArray[np.float64] = None, velocity:
    NDArray[np.float64] = None, acceleration: NDArray[np.float64] = None, angular_velocity: NDArray[np.float64] = None, angular_acceleration: NDArray[np.float64] = None):
        self.position = position
        self.rotation = rotation
        self.velocity = velocity
        self.acceleration = acceleration
        self.angular_velocity = angular_velocity
        self.angular_acceleration = angular_acceleration
        self.mass = mass
        self._length = length
        self._radius = radius
        self._inertia_tensor = self.calculate_inertia_tensor()

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
    def angular_velocity(self):
        return self._angular_velocity

    @angular_velocity.setter
    def angular_velocity(self, angular_velocity: NDArray[np.float64]):
        if angular_velocity is None:
            angular_velocity = np.array([0, 0, 0], dtype=np.float64)

        self._angular_velocity = angular_velocity

    @property
    def angular_acceleration(self):
        return self._angular_acceleration

    @angular_acceleration.setter
    def angular_acceleration(self, angular_acceleration: NDArray[np.float64]):
        if angular_acceleration is None:
            angular_acceleration = np.array([0, 0, 0], dtype=np.float64)

        self._angular_acceleration = angular_acceleration

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: NDArray[np.float64]):
        if velocity is None:
            velocity = np.array([0, 0, 0], dtype=np.float64)

        self._velocity = velocity

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass):
        self._mass = mass

    @property
    def length(self):
        return self._length

    @property
    def radius(self):
        return self._radius

    @property
    def inertia_tensor(self):
        return self._inertia_tensor

    def calculate_inertia_tensor(self):
        Ix = 1 / 12 * self.mass * (3 * self.radius ** 2 + self.length ** 2)
        Iy = 1 / 12 * self.mass * (3 * self.radius ** 2 + self.length ** 2)
        Iz = 1 / 2 * self.mass * self.radius ** 2
        return np.array([[Ix, 0, 0],
                         [0, Iy, 0],
                         [0, 0, Iz]])

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
