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

    wind_velocity_global = environment.get_wind(time)

    if (wind_velocity_global == np.array([0, 0, 0], dtype=float)).all():
        return np.array([0, 0, 0], dtype=float), np.array([0, 0, 0], dtype=float)
    wind_force_g = (0.5 * environment.get_air_density() * object.drag_coefficient * object.reference_area *
                  np.linalg.norm(wind_velocity_global) ** 2) * (
                             wind_velocity_global / np.linalg.norm(wind_velocity_global))
    wind_force_local = transform_to_local(wind_force_g, object.rotation)
    torque = np.cross(wind_force_local, np.array([0, 0, -object.cop], dtype=float))
    return wind_force_local, torque


