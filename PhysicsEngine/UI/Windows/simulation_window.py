import math
import os

import trimesh
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
from pyqtgraph.opengl import GLMeshItem

from PhysicsEngine.UI.Services.Timer import TimeLine
from PyQt5.QtCore import Qt
from PhysicsEngine.Utils import calculate_vector_magnitude
from ..Models import SimulationData
from ..Widgets.text_box import TextBox


class SimulationWindow(QtWidgets.QWidget):
    def __init__(self, file_path: str, camera_distance: int = 10):
        super().__init__()

        self.base_path = os.path.dirname(__file__)

        # CONFIG
        self.camera_distance = camera_distance

        # WINDOW SETUP
        self.setWindowTitle("Simulation Window")
        self.setWindowState(Qt.WindowMaximized)

        # DATA SETUP
        self.sim_data = SimulationData(file_path)
        # WIDGETS
        # 3D View
        self.view = gl.GLViewWidget()
        self.view.setCameraPosition(distance=self.camera_distance)  # Adjusted for better view
        grid = gl.GLGridItem()
        grid.setSize(20, 20)
        self.view.addItem(grid)

        # Change color and size of rocket point (make it larger and different color)
        # self.rocket_point = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]), color=(1, 0, 0, 1),
        #                                          size=10)  # Adjusted size
        self.rocket = self.load_model(os.path.join(self.base_path, "rocket.obj"))
        self.rocket_position = np.array([0, 0, 0])
        self.trajectory_line = gl.GLLinePlotItem(pos=np.array([[0, 0, 0]]), color=(0, 0, 1, 1), width=2)
        # self.view.addItem(self.rocket_point)
        self.view.addItem(self.trajectory_line)
        self.view.addItem(self.rocket)

        self.data_box = TextBox()
        self.data_box.add_text_widget("time", "Time: 0 s")
        self.data_box.add_text_widget("altitude", "Altitude: 0 m")
        self.data_box.add_text_widget("velocity", "Velocity: 0 m/s")
        self.data_box.add_text_widget("acceleration", "Acceleration: 0 m/s^2")

        # Layouts
        layout = QtWidgets.QHBoxLayout(self)
        graph_layout = QtWidgets.QVBoxLayout()


        layout.addWidget(self.data_box)
        layout.addWidget(self.view, 2)
        layout.addLayout(graph_layout, 1)  # Side graphs

        self.setLayout(layout)

        # Data graphs
        self.velocity_curve_dict = self.add_plot(graph_layout, "Velocity", "Time", "Velocity", ["r", "g", "b"],
                                                 ["Velocity X", "Velocity Y", "Velocity Z"])
        self.acceleration_curve_dict = self.add_plot(graph_layout, "Acceleration", "Time", "Acceleration",
                                                     ["r", "g", "b"],
                                                     ["Acceleration X", "Acceleration Y", "Acceleration Z"])
        self.altitude_curve = self.add_plot(graph_layout, "Altitude", "Time", "Altitude", "r", "Altitude")

        # Timer for 3D animation and 2D plot sync
        self._timeline = TimeLine(loopCount=0, interval=int(1000 * self.sim_data.time_step))
        self._timeline.setFrameRange(0, self.sim_data.data_points - 1)
        self._timeline.frameChanged.connect(self.update_trajectory)

        self._timeline.start()

        # Add Pause Button
        self.pause_button = QtWidgets.QPushButton('Pause')
        self.pause_button.clicked.connect(self.toggle_pause)
        graph_layout.addWidget(self.pause_button)

        # Add Slider to control the animation
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, self.sim_data.data_points - 1)  # Frame range
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.slider_value_changed)
        graph_layout.addWidget(self.slider)

        # Sync slider with animation
        self._timeline.frameChanged.connect(self.sync_slider_with_animation)

    def load_model(self, model_path):
        """Loads a 3D model using trimesh and adds its components to the scene."""
        try:
            # Load the 3D model
            mesh = trimesh.load(model_path)

            if isinstance(mesh, trimesh.Scene):
                # 1. Get all meshes in the scene
                meshes = list(mesh.geometry.values())

                # 2. Combine meshes into a single mesh
                mesh = trimesh.util.concatenate(meshes)

            # 3. Get the bounding box (used for translation and scaling)
            min_bound, max_bound = mesh.bounds  # This combines the bounds of the combined mesh

            # 4. Translate to center at (0, 0, 0)
            scene_center = (min_bound + max_bound) / 2
            mesh.apply_translation(-scene_center)  # Translate the combined mesh

            # 6. Scale the combined mesh to a desired height (for example, height = 0.5)
            current_height = max_bound[2] - min_bound[2]  # Height along z-axis
            desired_height = 0.5
            scale_factor = desired_height / current_height

            # Apply the scale to the combined mesh
            mesh.apply_scale(scale_factor)

            vertices = np.array(mesh.vertices, dtype=np.float32)
            faces = np.array(mesh.faces, dtype=np.int32)

            # Create the GLMeshItem
            mesh_item = GLMeshItem(
                vertexes=vertices,
                faces=faces,
                smooth=True,  # Enable smooth shading
                color=(1, 1, 1, 1),  # RGBA color for the model
                # drawEdges=True  # Draw edges for better visibility
            )
            mesh_item.setGLOptions('opaque')

            return mesh_item

        except Exception as e:
            print(f"Error loading model: {e}")

    def add_plot(self, parent, title: str, x_label: str, y_label: str, pen: str | list[str], name: str | list[str],
                 legend: bool = True):
        plot = pg.PlotWidget(title=title)
        parent.addWidget(plot)
        plot.setLabel('bottom', x_label)
        plot.setLabel('left', y_label)
        if legend:
            plot.addLegend()

        if isinstance(pen, list) and isinstance(name, list):
            dictionary = {}
            for p, n in zip(pen, name):
                dictionary[n] = plot.plot(pen=p, name=n)
            return dictionary

        return plot.plot(pen=pen, name=name)



    @QtCore.pyqtSlot(int)
    def update_trajectory(self, i):
        # Update rocket point position (change it to the current position)
        # self.rocket_point.setData(pos=np.array([self.sim_data.position_data[i]]))  # Update rocket position
        self.trajectory_line.setData(pos=self.sim_data.position_data[:i + 1])  # Update trajectory
        translate_matrix = self.sim_data.position_data[i] - self.rocket_position
        self.rocket_position = self.sim_data.position_data[i]
        self.rocket.translate(translate_matrix[0], translate_matrix[1], translate_matrix[2])


        # Update velocity and acceleration graphs
        self.velocity_curve_dict["Velocity X"].setData(self.sim_data.velocity_data[0][:i + 1])
        self.velocity_curve_dict["Velocity Y"].setData(self.sim_data.velocity_data[1][:i + 1])
        self.velocity_curve_dict["Velocity Z"].setData(self.sim_data.velocity_data[2][:i + 1])

        self.acceleration_curve_dict["Acceleration X"].setData(self.sim_data.acceleration_data[0][:i + 1])
        self.acceleration_curve_dict["Acceleration Y"].setData(self.sim_data.acceleration_data[1][:i + 1])
        self.acceleration_curve_dict["Acceleration Z"].setData(self.sim_data.acceleration_data[2][:i + 1])

        self.altitude_curve.setData(self.sim_data.position_data[:i + 1, 2])

        self.update_camera_position(i)

        # Update time text
        current_time = i * self.sim_data.time_step
        current_velocity = calculate_vector_magnitude(self.sim_data.velocity_data[:, i])
        current_altitude = self.sim_data.position_data[i, 2]
        current_acceleration = calculate_vector_magnitude(self.sim_data.acceleration_data[:, i])

        text_dict: dict = {
            "time": f"Time: {current_time:.2f} s",
            "velocity": f"Velocity: {current_velocity:.2f} m/s",
            "acceleration": f"Acceleration: {current_acceleration:.2f} m/s",
            "altitude": f"Altitude: {current_altitude:.2f} m",
        }

        self.data_box.update_multiple_widgets(text_dict)

    def update_camera_position(self, tick: int):
        obj_position = np.array(self.sim_data.position_data[tick])
        obj_position[2] = obj_position[2] / 2
        pos = pg.Vector(*obj_position)

        distance = int(self.camera_distance)
        computed = (obj_position[2]) / math.tan(math.radians(45))
        print(distance, computed)
        if computed > distance:
            distance = computed

        self.view.setCameraPosition(pos=pos, distance=distance, rotation=pg.Vector(0,0,0,False))

    def sync_slider_with_animation(self, frame):
        self.slider.setValue(frame)

    def toggle_pause(self):
        if self._timeline.paused:
            self._timeline.resume()
            self.pause_button.setText('Pause')
        else:
            self._timeline.pause()
            self.pause_button.setText('Resume')

    def slider_value_changed(self, value):
        # Manually change frame based on slider
        self._timeline._counter = value
        self.update_trajectory(value)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.toggle_pause()
