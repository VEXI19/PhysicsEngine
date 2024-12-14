import numpy as np
from numpy.typing import NDArray
import os
import datetime
from ..Object.IObject import IObject
from ..Environment.IEnvironment import IEnvironment
import progressbar
from ..Utils.EulerAngles import transform_to_local, transform_to_global


class PhysicsEngine:
    def __init__(self, object: IObject, environment: IEnvironment, time_step: float, max_simulation_time: float = 100.0, file_path: str = "./Simulations", file_name: str = "simulation"):
        self.object: IObject = object
        self.environment: IEnvironment = environment
        self.time_step: float = time_step
        self.pipeline: NDArray = np.array([])
        self.simulation_time: float = 0
        self.simulation_tick: int = 0
        self.file_path: str = file_path
        self.file_name: str = file_name
        self.max_simulation_time: float = max_simulation_time

    def next_tick(self):
        self.simulation_time += self.time_step
        self.simulation_tick += 1

    def get_config_data(self):
        return f"{self.time_step}"

    def add_force(self, force):
        self.pipeline = np.append(self.pipeline, force)

    def compute_force(self):
        resulting_force = np.array([0, 0, 0], dtype=float)
        resulting_torque = np.array([0, 0, 0], dtype=float)

        for force in self.pipeline:
            resulting_force += force(self.object, self.environment, self.simulation_time)[0]
            resulting_torque += force(self.object, self.environment, self.simulation_time)[1]

        return resulting_force, resulting_torque

    def compute_relative_values(self, resulting_force: NDArray[np.float64], resulting_torque: NDArray[np.float64]):
        # @VEXI19 - tutaj obliczamy predkosc wzgledna i przyspieszenie wzgledne dla algorytmu
        relative_acceleration = resulting_force / self.object.mass
        relative_velocity = transform_to_local(self.object.velocity, self.object.rotation) + relative_acceleration * self.time_step

        return relative_velocity, relative_acceleration

    def compute_change(self, force: NDArray[np.float64], torque: NDArray[np.float64]):

        global_force = transform_to_global(force, self.object.rotation)
        self.object.acceleration = global_force / self.object.mass
        velocity_change = self.object.acceleration * self.time_step
        position_change = velocity_change * self.time_step

        self.object.velocity += velocity_change
        self.object.position += position_change

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





    def save_data(self, data):
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)

        with open(f"{self.file_path}/{self.file_name}", "a") as file:
            file.write(f"{data}\n")

    def start(self):
        print("Initializing simulation")
        self.file_name = f"{self.file_name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        print(f"Saving initial data to file {self.file_name}")
        self.save_data(self.get_config_data())
        self.save_data("sim_tick,sim_time,pos_x,pos_y,pos_z,rot_x,rot_y,rot_z,vel_x,vel_y,vel_z,acc_x,acc_y,acc_z,mass")
        self.save_data(f"{self.simulation_tick},{self.simulation_time},{self.object.get_data()}")

        print("Starting simulation")

        bar = progressbar.ProgressBar(max_value=int(self.max_simulation_time / self.time_step))
        while self.object.position[2] >= 0 and self.simulation_time < self.max_simulation_time:
            bar.update(self.simulation_tick)

            resulting_force, resulting_torque = self.compute_force()
            self.compute_change(resulting_force, resulting_torque)
            self.next_tick()
            self.save_data(f"{self.simulation_tick},{self.simulation_time},{self.object.get_data()}")

        print("\nSimulation ended")
