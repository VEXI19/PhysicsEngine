from ..Object.IGravitational import IGravitational
from ..Environment.IEnvironment import IEnvironment
import numpy as np
from ..Utils import Constants


def gravity(object: IGravitational, environment: IEnvironment, time: float):
    return np.array([0, 0, -object.mass * Constants.GRAVITATIONAL_ACCELERATION.value], dtype=float)
