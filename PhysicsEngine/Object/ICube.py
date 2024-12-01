from abc import ABC
from ..Types import Vector3


class ICube(ABC):
    def __init__(self, dimensions: Vector3):
        self._dimensions = dimensions

    @property
    def dimensions(self):
        return self._dimensions
