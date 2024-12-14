import numpy as np


@staticmethod
def transform_to_global(local_vector, angles):
    """
    Transforms a vector from the local frame to the global frame.

    Args:
        local_vector (numpy.ndarray): Vector in the local frame [x, y, z].
        angles (numpy.ndarray): Euler angles in radians [roll, pitch, yaw].

    Returns:
        numpy.ndarray: Transformed vector in the global frame.
    """
    R = euler_to_rotation_matrix(angles)
    return R @ local_vector


@staticmethod
def transform_to_local(global_vector, angles):
    """
    Transforms a vector from the global frame to the local frame.

    Args:
        global_vector (numpy.ndarray): Vector in the global frame [x, y, z].
        angles (numpy.ndarray): Euler angles in radians [roll, pitch, yaw].

    Returns:
        numpy.ndarray: Transformed vector in the local frame.
    """
    R = euler_to_rotation_matrix(angles)
    return R.T @ global_vector


def euler_to_rotation_matrix(angles):
    """
    Computes the rotation matrix from Euler angles (Z-Y-X convention).

    Args:
        angles (numpy.ndarray): Euler angles in radians [roll, pitch, yaw].

    Returns:
        numpy.ndarray: 3x3 rotation matrix.
    """
    # Unpack angles (assumed in radians)
    fi1, fi2, fi3 = angles  # roll, pitch, yaw

    # Roll (x-axis rotation)
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(fi1), -np.sin(fi1)],
        [0, np.sin(fi1), np.cos(fi1)]
    ])

    # Pitch (y-axis rotation)
    Ry = np.array([
        [np.cos(fi2), 0, np.sin(fi2)],
        [0, 1, 0],
        [-np.sin(fi2), 0, np.cos(fi2)]
    ])

    # Yaw (z-axis rotation)
    Rz = np.array([
        [np.cos(fi3), -np.sin(fi3), 0],
        [np.sin(fi3), np.cos(fi3), 0],
        [0, 0, 1]
    ])

    # Combined rotation matrix (Z-Y-X order)
    R = Rz @ Ry @ Rx
    return R
