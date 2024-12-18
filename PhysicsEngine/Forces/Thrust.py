from ..Object.IThrust import IThrust
from ..Environment.IEnvironment import IEnvironment
import numpy as np
from ..Utils.EulerAngles import transform_to_global


def thrust(object: IThrust, environment: IEnvironment, time: float):

    thrust_mag = object.mass_flow_rate(time) * object.exhaust_velocity(time)
    thrust_v = np.array([0, 0, thrust_mag], dtype=float)
    thrust_g = transform_to_global(thrust_v, object.engine_angle)
    torque_l = np.cross(thrust_g, np.array([0, 0, object.cot], dtype=float))

    return thrust_g[2], torque_l
