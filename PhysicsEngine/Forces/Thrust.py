from ..Object.IThrust import IThrust
from ..Environment.IEnvironment import IEnvironment
import numpy as np
from ..Utils.EulerAngles import transform_to_global, transform_to_local


def thrust(object: IThrust, environment: IEnvironment, time: float):

    thrust_mag = object.mass_flow_rate(time) * object.exhaust_velocity(time)
    thrust_v = np.array([0, 0, thrust_mag], dtype=float)
    thrust_g = transform_to_global(thrust_v, object.engine_angle)
    torque_l = manual_cross(thrust_g, np.array([0, 0, -object.cot], dtype=float))
    # print(f"thrust: {thrust_g[2]}, torque {torque_l}")
    return thrust_g, torque_l


def manual_cross(a, b):
    return [
        a[1]*b[2] - a[2]*b[1],  # x-component
        a[2]*b[0] - a[0]*b[2],  # y-component
        a[0]*b[1] - a[1]*b[0]
    ]
