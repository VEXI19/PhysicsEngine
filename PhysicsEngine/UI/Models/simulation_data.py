import numpy as np
import pandas as pd
from numpy.typing import NDArray

class SimulationData:
    """
    Class for reading simulation data from a file and storing it in a structured way.

    Attributes:
        _time_step (float): time step of the simulation
        _position (NDArray): position data of the object
        _velocity (NDArray): velocity data of the object
        _acceleration (NDArray): acceleration data of the object
        _data_points (int): number of data points in the simulation (number of ticks in simulation)
        _starting_position (NDArray): starting position of the object
    """
    def __init__(self, file_path: str):
        """
        Constructor of SimulationData class

        Args:
            file_path (str): path to the file with simulation data
        """
        with open(file_path, 'r') as file:
            # reads first line with configuration information
            self._time_step: float = float(file.readline().strip())

            # reads simulation data
            data = pd.read_csv(file_path, skiprows=1)
            self._positions: NDArray = np.column_stack([data['pos_x'], data['pos_y'], data['pos_z']])
            self._velocities: NDArray = np.array([data['vel_x'], data['vel_y'], data['vel_z']])
            self._accelerations: NDArray = np.array([data['acc_x'], data['acc_y'], data['acc_z']])
            self._angular_accelerations: NDArray = np.array([data['ang_acc_x'], data['ang_acc_y'], data['ang_acc_z']])
            self._angular_velocities: NDArray = np.array([data['ang_vel_x'], data['ang_vel_y'], data['ang_vel_z']])
            self._rotations: NDArray = np.column_stack([data['rot_x'], data['rot_y'], data['rot_z']])
            self._data_points: int = len(self._positions)
            self._starting_position: NDArray = self._positions[0]

    @property
    def time_step(self) -> float:
        """
        Returns time step of the simulation

        Returns:
            float: time step of the simulation
        """

        return self._time_step

    @property
    def position_data(self) -> NDArray[np.float64]:
        """
        Returns position data of the object

        Returns:
            NDArray[np.float64]: position data of the object
        """
        return self._position

    @property
    def velocity_data(self) -> NDArray[np.float64]:
        """
        Returns velocity data of the object

        Returns:
            NDArray[np.float64]: velocity data of the object
        """

        return self._velocity

    @property
    def acceleration_data(self) -> NDArray[np.float64]:
        """
        Returns acceleration data of the object

        Returns:
            NDArray[np.float64]: acceleration data of the object
        """

        return self._acceleration

    @property
    def rotation_data(self) -> NDArray:
        return self._rotations

    @property
    def angular_acceleration_data(self) -> NDArray:
        return self._angular_accelerations

    @property
    def angular_velocity_data(self) -> NDArray:
        return self._angular_velocities

    @property
    def starting_position(self) -> NDArray[np.float64]:
        """
        Returns starting position of the object

        Returns:
            NDArray[np.float64]: starting position of the object
        """

        return self._starting_position

    @property
    def data_points(self) -> int:
        """
        Returns number of data points in the simulation (number of ticks in simulation)

        Returns:
            int: number of data points in the simulation
        """

        return self._data_points
