from ..Object.IObject import IObject
from ..Environment.IEnvironment import IEnvironment
import numpy as np
from ..Utils import Constants
from ..Utils.EulerAngles import transform_to_local


def gravity(object: IObject, environment: IEnvironment, time: float):
    global_gravity = np.array([0, 0, -object.mass * Constants.GRAVITATIONAL_ACCELERATION.value], dtype=float)
    local_gravity = transform_to_local(global_gravity, object.rotation)
    torque = np.array([0, 0, 0], dtype=float)
    return local_gravity, torque
