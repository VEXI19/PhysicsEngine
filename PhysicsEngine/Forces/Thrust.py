from ..Object.IThrust import IThrust
from ..Environment.IEnvironment import IEnvironment
import numpy as np
from numpy.typing import NDArray
from ..Utils.EulerAngles import transform_to_global, transform_to_local


def thrust(object: IThrust, environment: IEnvironment, time: float) -> (NDArray[np.float64], NDArray[np.float64]):
    """
    Function to compute thrust force and torque

    Args:
        object (IThrust): object on which thrust is acting
        environment (IEnvironment): simulation environment
        time (float): current time of the simulation

    Returns:
        (NDArray[np.float64], NDArray[np.float64]): thrust force and torque
    """

    thrust_mag = object.mass_flow_rate(time) * object.exhaust_velocity(time)
    thrust_v = np.array([0, 0, thrust_mag], dtype=float)
    thrust_g = transform_to_global(thrust_v, object.engine_angle)
    torque_l = np.cross(thrust_g, np.array([0, 0, -object.cot], dtype=float))
    return thrust_g, torque_l

