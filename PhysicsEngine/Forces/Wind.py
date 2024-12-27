from ..Object.IAerodependent import IAerodependent
from ..Environment.IEnvironment import IEnvironment
import numpy as np
from ..Utils.EulerAngles import transform_to_global, transform_to_local
from numpy.typing import NDArray


def wind(object: IAerodependent, environment: IEnvironment, time: float) -> (
        NDArray[np.float64], NDArray[np.float64]):
    """
    Function to compute wind force and torque

    Args:
        object (IAerodependent): object on which wind is acting
        environment (IEnvironment): simulation environment
        time (float): current time of the simulation

    Returns:
        (NDArray[np.float64], NDArray[np.float64]): wind force and torque
    """
    if (object.velocity == np.array([0, 0, 0], dtype=float)).all():
        return np.array([0, 0, 0], dtype=float), np.array([0, 0, 0], dtype=float)

    wind_v_global = environment.get_wind()
    wind_v_local = transform_to_local(wind_v_global, object.rotation)
    torque = np.cross(wind_v_local, np.array([0, 0, -object.cop], dtype=float))
    return wind_v_local, torque


