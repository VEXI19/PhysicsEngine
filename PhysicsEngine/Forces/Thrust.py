from ..Object.IThrust import IThrust
from ..Environment.IEnvironment import IEnvironment
import numpy as np
from ..Utils.EulerAngles import transform_to_global, transform_to_local


def thrust(object: IThrust, environment: IEnvironment, time: float):

    """
    Function to compute thrust force and torque
    @param object: object of the rocket with implemented IThrust interface
    @param environment: object of the environment with implemented IEnvironment interface
    @param time: current time of the simulation
    @return: thrust force and torque
    """

    thrust_mag = object.mass_flow_rate(time) * object.exhaust_velocity(time)
    thrust_v = np.array([0, 0, thrust_mag], dtype=float)
    thrust_g = transform_to_global(thrust_v, object.engine_angle)
    torque_l = np.cross(thrust_g, np.array([0, 0, -object.cot], dtype=float))
    return thrust_g, torque_l

