from ..Object.IAerodependent import IAerodependent
from ..Environment.IEnvironment import IEnvironment
import numpy as np
from ..Utils.EulerAngles import transform_to_global, transform_to_local
from numpy.typing import NDArray


def lift(object: IAerodependent, environment: IEnvironment, time: float) -> (
        NDArray[np.float64], NDArray[np.float64]):
    """
    Function to compute lift force and torque

    Args:
        object (IAerodependent): object on which lift is acting
        environment (IEnvironment): simulation environment
        time (float): current time of the simulation

    Returns:
        (NDArray[np.float64], NDArray[np.float64]): lift force and torque
    """
    if (object.velocity == np.array([0, 0, 0], dtype=float)).all():
        return np.array([0, 0, 0], dtype=float), np.array([0, 0, 0], dtype=float)

    Cl = object.lift_coefficient
    relative_velocity = object.relative_velocity
    reference_area = object.reference_area
    air_density = environment.get_air_density()
    lift_mag = 0.5 * air_density * np.linalg.norm(
        relative_velocity) ** 2 * Cl * reference_area
    velocity_unit = relative_velocity / np.linalg.norm(relative_velocity)
    lift_direction = np.cross(velocity_unit, np.array([0, 0, 1]))
    if np.linalg.norm(lift_direction) == 0:
        lift_direction = np.array([0, 1, 0])
    lift_v = lift_mag * lift_direction / np.linalg.norm(lift_direction)
    lift_l = transform_to_local(lift_v, object.rotation)
    torque = np.cross(lift_l, np.array([0, 0, -object.cop], dtype=float))

    return lift_l, torque