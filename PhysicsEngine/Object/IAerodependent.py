from abc import ABC, abstractmethod
import numpy as np
from .IObject import IObject

class IAerodependent(ABC):
    def __init__(self):
        self._reference_area = self.calculate_reference_area()

        if not isinstance(self, IObject):
            raise RuntimeError("Object needs to extend IObject to be IAerodependent")

    @property
    def reference_area(self):
        return self._reference_area

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