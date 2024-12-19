from ..Object.IAerodependent import IAerodependent
from ..Environment.IEnvironment import IEnvironment
import numpy as np
from ..Utils.EulerAngles import transform_to_global, transform_to_local


def drag(object: IAerodependent, environment: IEnvironment, time: float):
    """
    Function to compute drag force and torque
    @param object: object of the rocket with implemented IAerodependent interface
    @param environment: object of the environment with implemented IEnvironment interface
    @param time: current time of the simulation
    @return: drag force and torque
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

