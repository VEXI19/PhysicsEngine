import math
import os
import pickle

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
from ... import PhysicsEngine


class SimulationWindow(QtWidgets.QWidget):
    def __init__(self, file_path: str, camera_distance: int = 10):
        super().__init__()

        self.base_path = os.path.dirname(__file__)

        self.object_path = os.path.join(os.path.relpath(os.path.join(file_path, "..", "..")), "physics_engine.pkl")
        with open(self.object_path, "rb") as f:
            physics_engine: PhysicsEngine = pickle.load(f)
            self.object = physics_engine.object

        self.object_model = self.object.object_model

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
        self.view.setCameraPosition(distance=self.camera_distance)  # Adjusted for better vie
        self.view.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        grid = gl.GLGridItem()
        grid.setSize(20, 20)
        self.view.addItem(grid)

        # Change color and size of rocket point (make it larger and different color)
        # self.rocket_point = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]), color=(1, 0, 0, 1),
        #                                          size=10)  # Adjusted size

        vertices = np.array(self.object_model.vertices, dtype=np.float32)
        faces = np.array(self.object_model.faces, dtype=np.int32)

        # Create the GLMeshItem
        self.object_mesh_item = GLMeshItem(
            vertexes=vertices,
            faces=faces,
            # smooth=True,
            color=(1, 1, 1, 1),
        )
        self.object_mesh_item.setGLOptions('opaque')

        self.trajectory_line = gl.GLLinePlotItem(pos=np.array([[0, 0, 0]]), color=(0, 0, 1, 1), width=2)
        self.view.addItem(self.trajectory_line)
        self.view.addItem(self.object_mesh_item)

        self.data_box = TextBox()
        self.data_box.add_text_widget("time", "Time: 0 s")
        self.data_box.add_text_widget("altitude", "Altitude: 0 m")
        self.data_box.add_text_widget("velocity", "Velocity: 0 m/s")
        self.data_box.add_text_widget("acceleration", "Acceleration: 0 m/s^2")
        self.data_box.add_text_widget("angular_acceleration", "Angular acceleration: 0 rad/s^2")
        self.data_box.add_text_widget("angular_velocity", "Angular velocity: 0 rad/s")

        # Layouts
        layout = QtWidgets.QGridLayout(self)
        graph_layout_right = QtWidgets.QVBoxLayout()
        graph_layout_left = QtWidgets.QHBoxLayout()

        layout.setRowStretch(0, 1)  # Row 0 (graph_layout_left) gets a stretch factor of 1
        layout.setRowStretch(1, 1)  # Row 1 (main_layout) gets a stretch factor of 1
        layout.setRowStretch(2, 1)  # Row 1 (main_layout) gets a stretch factor of 1

        # Set column stretch factors
        layout.setColumnStretch(0, 1)  # Column 0 (graph_layout_left + main_layout) gets a stretch factor of 1
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(self.view, 0, 0)
        main_layout.addWidget(self.data_box, 0, 0)

        layout.addLayout(main_layout, 0, 0, 2, 2)
        layout.addLayout(graph_layout_left, 2, 0, 1, 2)
        layout.addLayout(graph_layout_right, 0, 2, 3, 1)

        self.setLayout(layout)

        # Data graphs
        self.velocity_curve_dict = self.add_plot(graph_layout_right, "Velocity", "Time [s]", "Velocity [m/s]", ["r", "g", "b"],
                                                 ["Velocity X", "Velocity Y", "Velocity Z"])
        self.acceleration_curve_dict = self.add_plot(graph_layout_right, "Acceleration", "Time [s]", "Acceleration [m/s^2]",
                                                     ["r", "g", "b"],
                                                     ["Acceleration X", "Acceleration Y", "Acceleration Z"])
        self.altitude_curve = self.add_plot(graph_layout_right, "Altitude", "Time [s]", "Altitude [m]", "r", "Altitude")

        self.angular_acceleration_curve_dict = self.add_plot(graph_layout_left, "Angular acceleration", "Time [s]", "Angular acceleration [rad/s^2]",
                                                             ["r", "g", "b"],
                                                             ["Angular acceleration X", "Angular acceleration Y", "Angular acceleration Z"])
        self.angular_velocity_curve_dict = self.add_plot(graph_layout_left, "Angular velocity", "Time [s]", "Velocity [rad/s]",
                                                         ["r", "g", "b"],
                                                         ["Angular velocity X", "Angular velocity Y", "Angular velocity Z"])

        # Add Pause Button
        self.pause_button = QtWidgets.QPushButton('Pause')
        self.pause_button.clicked.connect(self.toggle_pause)
        graph_layout_right.addWidget(self.pause_button)

        # Add Slider to control the animation
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, self.sim_data.data_points - 1)  # Frame range
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.slider_value_changed)
        graph_layout_right.addWidget(self.slider)

        # Timer for 3D animation and 2D plot sync
        self._timeline = TimeLine(loopCount=0, interval=int(1000 * self.sim_data.time_step))
        self._timeline.setFrameRange(0, self.sim_data.data_points - 1)
        self._timeline.frameChanged.connect(self.update_trajectory)

        self._timeline.start()

        # Sync slider with animation
        self._timeline.frameChanged.connect(self.sync_slider_with_animation)

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
        plot_time_axes = list(map(lambda x: x * self.sim_data.time_step, range(i)))

        self.trajectory_line.setData(pos=self.sim_data.position_data[:i])

        # update rocket position and rotation
        self.object_mesh_item.resetTransform()
        transform_matrix = self.sim_data.rotation_data[i]
        self.object_mesh_item.rotate(np.degrees(transform_matrix[0]), 1, 0, 0)
        self.object_mesh_item.rotate(np.degrees(transform_matrix[1]), 0, 1, 0)
        self.object_mesh_item.rotate(np.degrees(transform_matrix[2]), 0, 0, 1)
        self.object_mesh_item.translate(self.sim_data.position_data[i][0], self.sim_data.position_data[i][1], self.sim_data.position_data[i][2])

        # Update velocity and acceleration graphs
        self.velocity_curve_dict["Velocity X"].setData(plot_time_axes, self.sim_data.velocity_data[0][:i])
        self.velocity_curve_dict["Velocity Y"].setData(plot_time_axes, self.sim_data.velocity_data[1][:i])
        self.velocity_curve_dict["Velocity Z"].setData(plot_time_axes, self.sim_data.velocity_data[2][:i])

        self.acceleration_curve_dict["Acceleration X"].setData(plot_time_axes, self.sim_data.acceleration_data[0][:i])
        self.acceleration_curve_dict["Acceleration Y"].setData(plot_time_axes, self.sim_data.acceleration_data[1][:i])
        self.acceleration_curve_dict["Acceleration Z"].setData(plot_time_axes, self.sim_data.acceleration_data[2][:i])

        self.angular_acceleration_curve_dict["Angular acceleration X"].setData(plot_time_axes, self.sim_data.angular_acceleration_data[0][:i])
        self.angular_acceleration_curve_dict["Angular acceleration Y"].setData(plot_time_axes, self.sim_data.angular_acceleration_data[1][:i])
        self.angular_acceleration_curve_dict["Angular acceleration Z"].setData(plot_time_axes, self.sim_data.angular_acceleration_data[2][:i])

        self.angular_velocity_curve_dict["Angular velocity X"].setData(plot_time_axes, self.sim_data.angular_velocity_data[0][:i])
        self.angular_velocity_curve_dict["Angular velocity Y"].setData(plot_time_axes, self.sim_data.angular_velocity_data[1][:i])
        self.angular_velocity_curve_dict["Angular velocity Z"].setData(plot_time_axes, self.sim_data.angular_velocity_data[2][:i])

        self.altitude_curve.setData(plot_time_axes, self.sim_data.position_data[:i, 2])

        # self.update_camera_position(i)

        # Update time text
        current_time = i * self.sim_data.time_step
        current_velocity = calculate_vector_magnitude(self.sim_data.velocity_data[:, i])
        current_altitude = self.sim_data.position_data[i, 2]
        current_acceleration = calculate_vector_magnitude(self.sim_data.acceleration_data[:, i])
        current_angular_acceleration = calculate_vector_magnitude(self.sim_data.angular_acceleration_data[:, i])
        current_angular_velocity = calculate_vector_magnitude(self.sim_data.angular_velocity_data[:, i])

        text_dict: dict = {
            "time": f"Time: {current_time:.2f} s",
            "velocity": f"Velocity: {current_velocity:.2f} m/s",
            "acceleration": f"Acceleration: {current_acceleration:.2f} m/s",
            "altitude": f"Altitude: {current_altitude:.2f} m",
            "angular_acceleration": f"Angular acceleration: {current_angular_acceleration:.2f} rad/s^2",
            "angular_velocity": f"Angular velocity: {current_angular_velocity:.2f} rad/s",
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

        self.view.setCameraPosition(pos=pos, distance=distance)

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
