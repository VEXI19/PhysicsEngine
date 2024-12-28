from ..Object.IAerodependent import IAerodependent
from ..Environment.IEnvironment import IEnvironment
import numpy as np
from ..Utils.EulerAngles import transform_to_global, transform_to_local
from numpy.typing import NDArray


def calculate_wind_reference_area(object: IAerodependent, wind_velocity: NDArray[np.float64]) -> float:
    """
    Function to calculate the reference area based on wind direction.

    Args:
        object (IAerodependent): Object on which wind is acting.
        wind_velocity (NDArray[np.float64]): Wind velocity vector.

    Returns:
        float: Reference area for the wind force.
    """
    if np.linalg.norm(wind_velocity) == 0:
        return 0.0

    wind_direction = wind_velocity / np.linalg.norm(wind_velocity)
    projected = object.object_model.projected(wind_direction)

    return projected.area


def wind(object: IAerodependent, environment: IEnvironment, time: float) -> (
        NDArray[np.float64], NDArray[np.float64]):
    """
    Function to compute wind force and torque.

    Args:
        object (IAerodependent): Object on which wind is acting.
        environment (IEnvironment): Simulation environment.
        time (float): Current time of the simulation.

    Returns:
        (NDArray[np.float64], NDArray[np.float64]): Wind force and torque.
    """
    if (object.velocity == np.array([0, 0, 0], dtype=float)).all():
        return np.array([0, 0, 0], dtype=float), np.array([0, 0, 0], dtype=float)

    wind_velocity_global = environment.get_wind(time)

    if (wind_velocity_global == np.array([0, 0, 0], dtype=float)).all():
        return np.array([0, 0, 0], dtype=float), np.array([0, 0, 0], dtype=float)

    wind_area = calculate_wind_reference_area(object, wind_velocity_global)
    wind_force_g = (0.5 * environment.get_air_density() * object.drag_coefficient * wind_area *
                    np.linalg.norm(wind_velocity_global) ** 2) * (
                           wind_velocity_global / np.linalg.norm(wind_velocity_global))
    wind_force_local = transform_to_local(wind_force_g, object.rotation)
    torque = np.cross(wind_force_local, np.array([0, 0, -object.cop], dtype=float))

    return wind_force_local, torque
