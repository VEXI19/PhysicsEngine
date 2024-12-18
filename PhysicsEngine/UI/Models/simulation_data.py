import numpy as np
import pandas as pd
from numpy.typing import NDArray

class SimulationData:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            # reads first line with configuration information
            self._time_step: float = float(file.readline().strip())

            # reads simulation data
            data = pd.read_csv(file_path, skiprows=1)
            self._positions: NDArray = np.column_stack([data['pos_x'], data['pos_y'], data['pos_z']])
            self._velocities: NDArray = np.array([data['vel_x'], data['vel_y'], data['vel_z']])
            self._accelerations: NDArray = np.array([data['acc_x'], data['acc_y'], data['acc_z']])
            self._data_points: int = len(self._positions)
            self._starting_position: NDArray = self._positions[0]

    @property
    def time_step(self) -> float:
        return self._time_step

    @property
    def position_data(self) -> NDArray:
        return self._positions

    @property
    def velocity_data(self) -> NDArray:
        return self._velocities

    @property
    def acceleration_data(self) -> NDArray:
        return self._accelerations

    @property
    def starting_position(self) -> NDArray:
        return self._starting_position

    @property
    def data_points(self) -> int:
        return self._data_points
