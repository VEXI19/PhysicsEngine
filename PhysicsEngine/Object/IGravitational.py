from abc import ABC


class IGravitational(ABC):
    def __init__(self, mass):
        self.mass = mass
