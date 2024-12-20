from ..Object.IObject import IObject
from ..Environment.IEnvironment import IEnvironment
import numpy as np
from numpy.typing import NDArray
from ..Utils import Constants
from ..Utils.EulerAngles import transform_to_local


def gravity(object: IObject, environment: IEnvironment, time: float) -> (NDArray[np.float64], NDArray[np.float64]):
    """
    Function to compute gravity force and torque

    Args:
        object (IObject): object on which gravity is acting
        environment (IEnvironment): simulation environment
        time (float): current time of the simulation

    Returns:
        (NDArray[np.float64], NDArray[np.float64]): gravity force and torque
    """

    global_gravity = np.array([0, 0, -object.mass * Constants.GRAVITATIONAL_ACCELERATION.value], dtype=float)
    local_gravity = transform_to_local(global_gravity, object.rotation)
    torque = np.array([0, 0, 0], dtype=float)

    return local_gravity, torque
