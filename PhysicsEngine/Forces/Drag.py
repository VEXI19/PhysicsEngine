from ..Object.IAerodependent import IAerodependent
from ..Environment.IEnvironment import IEnvironment
import numpy as np
from ..Utils.EulerAngles import transform_to_global, transform_to_local
from numpy.typing import NDArray


def drag(object: IAerodependent, environment: IEnvironment, time: float) -> (NDArray[np.float64], NDArray[np.float64]):
    """
    Function to compute drag force and torque

    Args:
        object (IAerodependent): object on which drag is acting
        environment (IEnvironment): simulation environment
        time (float): current time of the simulation

    Returns:
        (NDArray[np.float64], NDArray[np.float64]): drag force and torque
    """
    if (object.velocity == np.array([0, 0, 0], dtype=float)).all():
        return np.array([0, 0, 0], dtype=float), np.array([0, 0, 0], dtype=float)

    Cd = object.drag_coefficient
    relative_velocity = object.relative_velocity
    reference_area = object.reference_area
    drag_mag = 0.5 * environment.get_air_density() * np.linalg.norm(relative_velocity) ** 2 * Cd * reference_area
    drag_v = -drag_mag * (relative_velocity / np.linalg.norm(relative_velocity))
    drag_l = transform_to_local(drag_v, object.rotation) # to jest git
    torque = np.cross(drag_l, np.array([0, 0, -object.cop], dtype=float))
    return drag_v, torque

