import os
from abc import ABC

import trimesh

import numpy as np
from numpy.typing import NDArray

from PhysicsEngine.Config import Config


class IObject(ABC):
    """
    Interface for objects in the simulation
    
    Attributes:
        name (str): name of the object
        position (NDArray[np.float64]): position of the object
        rotation (NDArray[np.float64]): rotation of the object
        velocity (NDArray[np.float64]): velocity of the object
        acceleration (NDArray[np.float64]): acceleration of the object
        angular_velocity (NDArray[np.float64]): angular velocity of the object
        angular_acceleration (NDArray[np.float64]): angular acceleration of the object
        mass (float): mass of the object
        object_model (trimesh.Trimesh): 3D model of the object
        _height (float): height of the object
        _radius (float): radius of the object
        _inertia_tensor (NDArray[np.float64]): inertia tensor of the object
    """
    def __init__(self, name: str, object_model_path: str, height: float, mass: float = 1,
                 radius: float = 0.1,  position: NDArray[np.float64] = None, rotation: NDArray[np.float64] = None, velocity:
    NDArray[np.float64] = None, acceleration: NDArray[np.float64] = None, angular_velocity: NDArray[np.float64] = None, angular_acceleration: NDArray[np.float64] = None):
        """
        Constructor for IObject class
        
        Args:
            name (str): name of the object
            object_model_path (str): path to the 3D model of the object
            height (float): height of the object
            mass (float): mass of the object
            radius (float): radius of the object
            position (NDArray[np.float64]): initial position of the object
            rotation (NDArray[np.float64]): initial rotation of the object
            velocity (NDArray[np.float64]): initial velocity of the object
            acceleration (NDArray[np.float64]): initial acceleration of the object
            angular_velocity (NDArray[np.float64]): initial angular velocity of the object
            angular_acceleration (NDArray[np.float64]): initial angular acceleration of the object
        """

        self._config = Config()

        self.name = name

        # GLOBAL
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

        # LOCAL
        self.angular_velocity = angular_velocity
        self.angular_acceleration = angular_acceleration
        self.rotation = rotation

        # NA
        self.mass = mass
        self._height = height
        self._radius = radius
        self._inertia_tensor = self.calculate_inertia_tensor()

        self.object_model = self.load_model(object_model_path)

    def load_model(self, object_model_path: str) -> None:
        """
        Loads a 3D model, scales it to height given in constructor and centers it in the scene.
        
        Args:
            object_model_path (str): path to the 3D model of the object
        """

        try:
            mesh = trimesh.load(object_model_path)

            if isinstance(mesh, trimesh.Scene):
                meshes = list(mesh.geometry.values())

                mesh = trimesh.util.concatenate(meshes)

            min_bound, max_bound = mesh.bounds

            # centers model and puts the bottom part on the ground
            bottom_center_translation = -min_bound  # Align bottom face to z=0
            bottom_center_translation[0] -= (max_bound[0] - min_bound[0]) / 2  # Center x-axis
            bottom_center_translation[1] -= (max_bound[1] - min_bound[1]) / 2  # Center y-axis
            mesh.apply_translation(bottom_center_translation)

            # scales model
            current_height = max_bound[2] - min_bound[2]
            scale_factor = self.height / current_height
            mesh.apply_scale(scale_factor)

            return mesh

        except Exception as e:
            print(f"Error loading model: {e}")

    # def calculate_diameter(self):
    #     # Define a plane equation for slicing along the z-axis
    #     # This plane will be of the form z = z_value
    #
    #     # Create a slicing plane (normal to the z-axis)
    #     plane_normal = np.array([0, 0, 1])
    #     plane_origin = np.array([0, 0, 0.2])  # The slicing plane at z = z_value
    #
    #     # Slice the 3D object using the plane
    #     section = self.object_model.section(plane_origin=plane_origin, plane_normal=plane_normal)
    #
    #     # Check if the object has an intersection with the slicing plane
    #     if section:
    #         # Create a 2D mesh or path from the section
    #         # section_mesh = trimesh.Trimesh(vertices=section.vertices)
    #         slice_2d: trimesh.path.Path2D = section.to_planar()[0]
    #         return slice_2d.length
    #     else:
    #         print(f"No intersection found with the plane at z =")
    #         return None

    @property
    def name(self) -> str:
        """
        Returns name of the object
        
        Returns:
            str: name of the object
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Sets name of the object
        
        Args:
            value (str): name of the object

        """
        simulations_path = self._config["SIMULATION"]["simulation_files_folder_path"]
        approved: str = ""
        if os.path.exists(simulations_path) and value in os.listdir(simulations_path):
            while approved.lower() != "y" and approved.lower() != "n":
                approved: str = input("Simulation with that name already exists, do you want to overwrite it? (y/n)")

            if approved.lower() == "n":
                exit(0)

        self._name = value

    @property
    def position(self) -> NDArray[np.float64]:
        """
        Returns position vector of the object
        
        Returns:
            NDArray[np.float64]: position vector of the object
        """
        return self._position

    @position.setter
    def position(self, position: NDArray[np.float64]) -> None:
        """
        Sets position vector of the object
        
        Args:
            position (NDArray[np.float64]): position vector

        """
        if position is None:
            position = np.array([0, 0, 0], dtype=np.float64)

        self._position = position

    @property
    def rotation(self) -> NDArray[np.float64]:
        """
        Returns rotation vector of the object
        
        Returns:
            NDArray[np.float64]: rotation vector of the object
        """
        
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: NDArray[np.float64]) -> None:
        """
        Sets rotation vector of the object
        
        Args:
            rotation (NDArray[np.float64]): rotation vector

        """
        
        if rotation is None:
            rotation = np.array([0, 0, 0], dtype=np.float64)

        self._rotation = rotation

    @property
    def acceleration(self) -> NDArray[np.float64]:
        """
        Returns acceleration vector of the object
        
        Returns:
            NDArray[np.float64]: acceleration vector of the object
        """
        
        return self._acceleration

    @acceleration.setter
    def acceleration(self, acceleration: NDArray[np.float64]) -> None:
        """
        Sets acceleration vector of the object
        
        Args:
            acceleration (NDArray[np.float64]): acceleration vector

        """
        
        if acceleration is None:
            acceleration = np.array([0, 0, 0], dtype=np.float64)

        self._acceleration = acceleration

    @property
    def angular_velocity(self) -> NDArray[np.float64]:
        """
        Returns angular velocity vector of the object
        
        Returns:
            NDArray[np.float64]: angular velocity vector of the object
        """
        
        return self._angular_velocity

    @angular_velocity.setter
    def angular_velocity(self, angular_velocity: NDArray[np.float64]) -> None:
        """
        Sets angular velocity vector of the object
        
        Args:
            angular_velocity (NDArray[np.float64]): angular velocity vector
        """
        
        if angular_velocity is None:
            angular_velocity = np.array([0, 0, 0], dtype=np.float64)

        self._angular_velocity = angular_velocity

    @property
    def angular_acceleration(self) -> NDArray[np.float64]:
        """
        Returns angular acceleration vector of the object
        
        Returns:
            NDArray[np.float64]: angular acceleration vector of the object
        """
        
        return self._angular_acceleration

    @angular_acceleration.setter
    def angular_acceleration(self, angular_acceleration: NDArray[np.float64]) -> None:
        """
        Sets angular acceleration vector of the object
        
        Args:
            angular_acceleration (NDArray[np.float64]): angular acceleration vector
        """
        
        if angular_acceleration is None:
            angular_acceleration = np.array([0, 0, 0], dtype=np.float64)

        self._angular_acceleration = angular_acceleration

    @property
    def velocity(self) -> NDArray[np.float64]:
        """
        Returns velocity vector of the object
        
        Returns:
            NDArray[np.float64]: velocity vector of the object
        """
        
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: NDArray[np.float64]) -> None:
        """
        Sets velocity vector of the object
        
        Args:
            velocity (NDArray[np.float64]): velocity vector

        """
        
        if velocity is None:
            velocity = np.array([0, 0, 0], dtype=np.float64)

        self._velocity = velocity

    @property
    def mass(self) -> float:
        """
        Returns mass of the object
        
        Returns:
            float: mass of the object
        """
        
        return self._mass

    @mass.setter
    def mass(self, mass) -> None:
        """
        Sets mass of the object
        
        Args:
            mass (float): mass

        """
        
        self._mass = mass

    @property
    def height(self) -> float:
        """
        Returns height of the object
        
        Returns:
            float: height of the object
        """
        
        return self._height

    @property
    def radius(self) -> float:
        """
        Returns radius of the object
        
        Returns:
            float: radius of the object
        """
        
        return self._radius

    @property
    def inertia_tensor(self) -> NDArray[np.float64]:
        """
        Returns inertia tensor of the object
        
        Returns:
            NDArray[np.float64]: inertia tensor of the object
        """
        return self._inertia_tensor

    def calculate_inertia_tensor(self) -> NDArray[np.float64]:
        """
        Function to calculate inertia tensor

        Returns:
            NDArray[np.float64]: inertia tensor of the object
        """
        Ix = 1 / 12 * self.mass * (3 * self.radius ** 2 + self.height ** 2)
        Iy = 1 / 12 * self.mass * (3 * self.radius ** 2 + self.height ** 2)
        Iz = 1 / 2 * self.mass * self.radius ** 2
        return np.array([[Ix, 0, 0],
                         [0, Iy, 0],
                         [0, 0, Iz]])

    def get_data_header(self):
        headers = "sim_tick,sim_time,mass,pos_x,pos_y,pos_z,rot_x,rot_y,rot_z,vel_x,vel_y,vel_z,acc_x,acc_y,acc_z,ang_vel_x,ang_vel_y,ang_vel_z,ang_acc_x,ang_acc_y,ang_acc_z"
        next_headers = super().get_data_header() if hasattr(super(), "get_data_header") else ""
        return f"{headers},{next_headers}"

    def get_data(self):
        """
        Function to get data used to save during simulation
        
        Returns:
            str: data used to save during simulation
        """
        
        data = f"{self.mass},{self.position[0]},{self.position[1]},{self.position[2]},{self.rotation[0]},{self.rotation[1]},{self.rotation[2]},{self.velocity[0]},{self.velocity[1]},{self.velocity[2]},{self.acceleration[0]},{self.acceleration[1]},{self.acceleration[2]}, {self.angular_velocity[0]},{self.angular_velocity[1]},{self.angular_velocity[2]},{self.angular_acceleration[0]},{self.angular_acceleration[1]},{self.angular_acceleration[2]}"
        next_data = super().get_data() if hasattr(super(), "get_data") else ""
        return f"{data},{next_data}"

