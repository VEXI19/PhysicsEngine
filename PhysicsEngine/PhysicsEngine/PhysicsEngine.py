import numpy as np
from numpy.typing import NDArray
import os
import datetime

from ..Utils.Constants import Constants as C
from ..Config import Config
from ..Object import IAerodependent
from ..Object.IObject import IObject
from ..Environment.IEnvironment import IEnvironment
import progressbar
from ..Utils.EulerAngles import transform_to_local, transform_to_global


class PhysicsEngine:
    """
    Class running the simulation. It computes forces and torques acting on the object and calculates its position,
    velocity, rotation and angular velocity.

    Attributes:
        object (IObject): object to simulate
        environment (IEnvironment): environment in which object is simulated
        time_step (float): time step of simulation
        force_pipeline (NDArray): pipeline of forces to apply
        simulation_time (float): current simulation time
        max_simulation_time (float): maximum simulation time
        simulation_tick (int): current simulation tick
        file_path (str): path to save simulation data
        file_name (str): name of file to save simulation data
    """

    def __init__(self, object: IObject, environment: IEnvironment, time_step: float, max_simulation_time: float = 100.0, file_name: str = "simulation"):
        """
        Constructor of PhysicsEngine class

        Args:
            object (IObject): object to simulate
            environment (IEnvironment): environment in which object is simulated
            time_step (float): time step of simulation
            max_simulation_time (float): time limitation of the simulation
            file_name (string): file name of the simulation data (date and time will be added to this name)
        """

        self.config = Config()

        self.object: IObject = object
        self.environment: IEnvironment = environment
        self.time_step: float = time_step
        self.force_pipeline: NDArray = np.array([])
        self.simulation_time: float = 0
        self.simulation_tick: int = 0
        self.file_path: str = self.config["SIMULATION"]["simulation_files_folder_path"]
        self.file_name: str = file_name
        self.max_simulation_time: float = max_simulation_time

    def next_tick(self) -> None:
        """
        Increments simulation time and simulation tick
        """

        self.simulation_time += self.time_step
        self.simulation_tick += 1

    def get_config_data(self) -> str:
        """
        Creates first line of simulation data file containing simulation configuration

        Returns:
            str: simulation config data
        """

        return f"{self.time_step},{self.max_simulation_time},{self.object.get_config_data()}"

    def add_force(self, force: callable) -> None:
        """
        Appends force function to the force pipeline

        Args:
            force (function): force function to append to the pipeline
        """

        self.force_pipeline = np.append(self.force_pipeline, force)

    def compute_force(self) -> (NDArray[np.float64], NDArray[np.float64]):
        """
        Computes resulting force and resulting torque from forces acting on an object

        Returns:
            (NDArray[np.float64], NDArray[np.float64]): tuple containing resulting force and resulting torque vectors
        """
        resulting_force = np.array([0, 0, 0], dtype=float)
        resulting_torque = np.array([0, 0, 0], dtype=float)

        for force in self.force_pipeline:
            resulting_force += force(self.object, self.environment, self.simulation_time)[0]
            resulting_torque += force(self.object, self.environment, self.simulation_time)[1]

        return resulting_force, resulting_torque

    def compute_relative_values(self, resulting_force: NDArray[np.float64], resulting_torque: NDArray[np.float64]):
        # TODO @VEXI19 - tutaj obliczamy predkosc wzgledna i przyspieszenie wzgledne dla algorytmu
        relative_acceleration = resulting_force / self.object.mass
        relative_velocity = transform_to_local(self.object.velocity, self.object.rotation) + relative_acceleration * self.time_step

        return relative_velocity, relative_acceleration

    def calculate_angle_of_attack(self) -> float:
        """
        Calculates angle of attack

        Returns:
            float: angle of attack
        """
        object_velocity = self.object.velocity
        wind_velocity = self.environment.get_wind()
        relative_velocity = object_velocity - wind_velocity
        relative_velocity_unit = relative_velocity / np.linalg.norm(relative_velocity)

        reference_axis_local = np.array([0, 0, 1], dtype=float)
        reference_axis_global = transform_to_global(reference_axis_local, self.object.rotation)

        cos_theta = np.dot(relative_velocity_unit, reference_axis_global)
        angle_of_attack = np.arccos(np.clip(cos_theta, -1.0, 1.0))

        return angle_of_attack

    def compute_change(self, force: NDArray[np.float64], torque: NDArray[np.float64]) -> None:
        """
        Calculates and saves changes in object's position, velocity, rotation, angular acceleration and angular velocity
        """
        relative_velocity, relative_acceleration = self.compute_relative_values(force, torque)
        self.object.relative_velocity = relative_velocity
        self.object.relative_acceleration = relative_acceleration

        global_force = transform_to_global(force, self.object.rotation)
        self.object.acceleration = global_force / self.object.mass
        velocity_change = self.object.acceleration * self.time_step
        self.object.velocity += velocity_change

        position_change = self.object.velocity * self.time_step
        self.object.position += position_change

        if isinstance(self.object, IAerodependent) and isinstance(self.object, IObject):
            self.object.angle_of_attack = self.calculate_angle_of_attack()
            self.object.relative_velocity = self.object.velocity - self.environment.get_wind()
            self.object.drag_coefficient = (C.DRAG_COEFFICIENT_PARALLEL.value * np.cos(self.object.angle_of_attack) **  2 + C.DRAG_COEFFICIENT_PERPENDICULAR.value * np.sin(self.object.angle_of_attack) ** 2)

        # obliczanie przyspieszenia katowego

        self.object.angular_acceleration = np.linalg.inv(self.object.inertia_tensor) @ torque
        self.object.angular_velocity += self.object.angular_acceleration * self.time_step

        wx, wy, wz = self.object.angular_velocity
        phi, theta, psi = self.object.rotation

        dot_phi = wx + (np.tan(theta) * np.sin(phi) * wy + np.cos(phi) * wz)
        dot_theta = np.cos(phi) * wy - np.sin(phi) * wz
        dot_psi = np.sin(phi) / np.cos(theta) * wy + np.cos(phi) * wz

        self.object.rotation[0] += dot_phi * self.time_step
        self.object.rotation[1] += dot_theta * self.time_step
        self.object.rotation[2] += dot_psi * self.time_step

        self.object.engine_angle = np.array([[0.05, 0.05, 0], [0.05, -0.05, 0], [-0.05, -0.05, 0], [-0.05, 0.05, 0]])[self.simulation_tick % 4]


    def save_data(self, data: str) -> None:
        """
        Saves given string to the simulation data file. Creates new line

        Args:
            data (str): data to save
        """

        path = os.path.join(self.file_path, self.object.name, "Simulations")

        if not os.path.exists(path):
            os.makedirs(path)

        with open(f"{path}/{self.file_name}", "a") as file:
            file.write(f"{data}\n")

    def start(self) -> None:
        """
        Starts simulation. Executes main loop of the simulation.
        """

        print("Initializing simulation")
        self.file_name = f"{self.file_name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        print(f"Saving initial data to file {self.file_name}")
        self.save_data(self.get_config_data())
        self.save_data(self.object.get_data_header())
        self.save_data(f"{self.simulation_tick},{self.simulation_time},{self.object.get_data()}")

        print("Starting simulation")

        bar = progressbar.ProgressBar(int(self.max_simulation_time / self.time_step)).start()
        while self.object.position[2] >= 0 and self.simulation_time < self.max_simulation_time:
            bar.update(self.simulation_tick)

            resulting_force, resulting_torque = self.compute_force()
            self.compute_change(resulting_force, resulting_torque)
            self.next_tick()
            self.save_data(f"{self.simulation_tick},{self.simulation_time},{self.object.get_data()}")

        print("\nSimulation ended")
