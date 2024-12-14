from ..Object.IThrust import IThrust
from ..Environment.IEnvironment import IEnvironment
import numpy as np


def thrust(object: IThrust, environment: IEnvironment, time: float):
    return np.array([0, 0, object.mass_flow_rate(time) * object.exhaust_velocity(time)]), np.array([0, 0.01, 0],
                                                                                                   dtype=float)
