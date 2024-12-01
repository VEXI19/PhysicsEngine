from ..Object import *


def aero(func):
    def wrapper(self, *args, **kwargs):
        if not isinstance(self.object, IAerodependent):
            raise Exception("Object does not implement IAerodependent")

        return func(self, *args, **kwargs)
    return wrapper


def grav(func):
    def wrapper(self, *args, **kwargs):
        if not isinstance(self.object, IGravitational):
            raise Exception("Object does not implement IGravitational")

        return func(self, *args, **kwargs)
    return wrapper


def thrust(func):
    def wrapper(self, *args, **kwargs):
        if not isinstance(self.object, IThrust):
            raise Exception("Object does not implement IThrust")

        return func(self, *args, **kwargs)
    return wrapper


def cube(func):
    def wrapper(self, *args, **kwargs):
        if not isinstance(self.object, ICube):
            raise Exception("Object does not implement ICube")

        return func(self, *args, **kwargs)
    return wrapper
