import os
from abc import ABC

import trimesh

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import leastsq

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
                 position: NDArray[np.float64] = None, rotation: NDArray[np.float64] = None, velocity:
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

        self.local_velocity = np.array([0, 0, 0])
        self.local_acceleration = np.array([0, 0, 0])

        # NA
        # self.imperfection_torque = np.random.normal(0, 0.007, 3)
        self.mass = mass
        self._height = height

        self.object_model = self.load_model(object_model_path)
        self._radius = self.calculate_radius()
        self._inertia_tensor = self.calculate_inertia_tensor()


    def load_model(self, object_model_path: str) -> trimesh.Trimesh:
        """
        Loads a 3D model, scales it to height given in constructor and centers it in the scene.
        
        Args:
            object_model_path (str): path to the 3D model of the object
        """

        mesh = trimesh.load(object_model_path)

        if isinstance(mesh, trimesh.Scene):
            meshes = list(mesh.geometry.values())

            mesh = trimesh.util.concatenate(meshes)

        if not mesh.is_watertight:
            mesh = mesh.convex_hull

        mesh.merge_vertices()

        # Remove degenerate (zero-area) faces
        # mesh.remove_degenerate_faces()
        #
        # # Fill holes and fix non-manifold edges
        # mesh.fill_holes()
        # mesh.remove_unreferenced_vertices()
        # mesh.remove_duplicate_faces()

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

        if isinstance(mesh, trimesh.Trimesh):
            # mesh.simplify_quadric_decimation(1000)
            mesh.remove_duplicate_faces()
            mesh.remove_degenerate_faces()

        return mesh


    def calculate_radius(self) -> float:
        """
        Calculates radius of the object based on 3d model and height

        Returns:
            float: radius of the object
        """

        z_extents = np.array(self.object_model.bounds[:, 2])
        diff = (z_extents[1] - z_extents[0]) * .25
        z_extents[0] = z_extents[0] + diff
        z_extents[1] = z_extents[1] - diff
        step = diff / 12
        z_levels = np.arange(*z_extents, step=step)

        # find a bunch of parallel cross sections
        sections = self.object_model.section_multiplane(
            plane_origin=self.object_model.bounds[0], plane_normal=[0, 0, 1], heights=z_levels
        )

        def fit_circle(points):
            def calc_radius(xc, yc):
                return np.sqrt((points[:, 0] - xc) ** 2 + (points[:, 1] - yc) ** 2)

            def residuals(center, points):
                radii = calc_radius(*center)
                return radii - radii.mean()

            # Initial guess for center
            x_m, y_m = points[:, 0].mean(), points[:, 1].mean()
            center_estimate = x_m, y_m

            # Fit circle
            center, _ = leastsq(residuals, center_estimate, args=(points,))
            radius = calc_radius(*center).mean()

            return center, radius

        radiuses = []

        for section in sections:
            if section is not None:
                center, radius = fit_circle(section.vertices)
                radiuses.append(radius)

        return float(np.median(radiuses))

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
        # simulations_path = self._config["SIMULATION"]["simulation_files_folder_path"]
        # approved: str = ""
        # if os.path.exists(simulations_path) and value in os.listdir(simulations_path):
        #     while approved.lower() != "y" and approved.lower() != "n":
        #         approved: str = input("Simulation with that name already exists, do you want to overwrite it? (y/n)")
        #
        #     if approved.lower() == "n":
        #         exit(0)

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

    def reset(self):
        """
        Function to reset object to initial state
        """
        self.position = np.array([0, 0, 0], dtype=np.float64)
        self.rotation = np.array([0, 0, 0], dtype=np.float64)
        self.velocity = np.array([0, 0, 0], dtype=np.float64)
        self.acceleration = np.array([0, 0, 0], dtype=np.float64)
        self.angular_velocity = np.array([0, 0, 0], dtype=np.float64)
        self.angular_acceleration = np.array([0, 0, 0], dtype=np.float64)
        self.local_velocity = np.array([0, 0, 0], dtype=np.float64)
        self.local_acceleration = np.array([0, 0, 0], dtype=np.float64)

    def get_data_header(self) -> str:
        """
        Returns headers for the simulation data

        Returns:
            string: headers for the simulation data
        """

        headers = "sim_tick,sim_time,mass,pos_x,pos_y,pos_z,rot_x,rot_y,rot_z,vel_x,vel_y,vel_z,acc_x,acc_y,acc_z,ang_vel_x,ang_vel_y,ang_vel_z,ang_acc_x,ang_acc_y,ang_acc_z"
        next_headers = super().get_data_header() if hasattr(super(), "get_data_header") else ""

        return f"{headers},{next_headers}"

    def get_data(self):
        """
        Function to get data used to save during simulation
        
        Returns:
            str: data used to save during simulation
        """

        data = f"{self.mass},{self.position[0]},{self.position[1]},{self.position[2]},{self.rotation[0]},{self.rotation[1]},{self.rotation[2]},{self.local_velocity[0]},{self.local_velocity[1]},{self.local_velocity[2]},{self.local_acceleration[0]},{self.local_acceleration[1]},{self.local_acceleration[2]}, {self.angular_velocity[0]},{self.angular_velocity[1]},{self.angular_velocity[2]},{self.angular_acceleration[0]},{self.angular_acceleration[1]},{self.angular_acceleration[2]}"
        next_data = super().get_data() if hasattr(super(), "get_data") else ""

        return f"{data},{next_data}"

    def get_data_config_header(self) -> str:
        """
        Returns headers for the configuration data of an object

        Returns:
            string: headers for the configuration data of an object
        """

        headers = "obj_name,obj_radius,obj_height"
        next_headers = super().get_data_config_header() if hasattr(super(), "get_data_header") else ""

        return f"{headers},{next_headers}"

    def get_config_data(self):
        """
        Function to get configuration data of an object

        Returns:
            str: configuration data of an object
        """

        data = f"{self.name},{self.radius},{self.height}"
        next_data = super().get_config_data() if hasattr(super(), "get_config_data") else ""

        return f"{data},{next_data}"