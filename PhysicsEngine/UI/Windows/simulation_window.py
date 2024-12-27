import math
import os
import pickle
from collections.abc import Sequence

import trimesh
from PyQt5 import QtCore, QtWidgets, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QPushButton, QComboBox, QLabel
from numpy.lib.function_base import quantile
from pyqtgraph.opengl import GLMeshItem

from PhysicsEngine.UI.Services.Timer import TimeLine
from PyQt5.QtCore import Qt, QItemSelection
from PhysicsEngine.Utils import calculate_vector_magnitude
from ..Models import SimulationData
from ..Widgets.text_box import TextBox
from ... import PhysicsEngine
from ...Config import Config


class SimulationWindow(QtWidgets.QWidget):
    """
    SimulationWindow class is a QWidget class that displays the simulation data in a 3D view and 2D graphs.
    """

    def __init__(self, file_path: str, camera_distance: int = 10):
        super().__init__()

        self.config = Config()
        self.base_path = os.path.dirname(__file__)

        self.object_path = os.path.join(os.path.relpath(os.path.join(file_path, "..", "..")), "physics_engine.pkl")
        with open(self.object_path, "rb") as f:
            physics_engine: PhysicsEngine = pickle.load(f)
            self.object = physics_engine.object

        self.object_model = self.object.object_model

        # CAMERA
        self.camera_distance = camera_distance
        self.camera_mode = int(self.config["SIMULATION"]["camera_mode"])

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

        # Camera following picker
        self.camera_mode_select = QComboBox()
        self.camera_mode_select.addItems(['Follow', 'POV', 'Landscape', 'Free'])
        self.camera_mode_select.setCurrentIndex(self.camera_mode)

        self.camera_mode_select.currentIndexChanged.connect(self.camera_mode_change)

        self.camera_mode_layout = QtWidgets.QHBoxLayout()
        self.camera_mode_layout.addWidget(QLabel("Camera Mode:"))
        self.camera_mode_layout.addWidget(self.camera_mode_select)

        graph_layout_right.addLayout(self.camera_mode_layout)

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
        self.engine_angle_point = self.add_scatter_plot(graph_layout_left, "Engine angle", "Angle X [rad]",
                                                         "Angle Y [rad]",
                                                        "o",
                                                         "r",
                                                            10,
                                                         "Engine angle", (-.5, .5), (-.5, .5))

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
        self._timeline = TimeLine(loop_count=0, interval=int(1000 * self.sim_data.time_step))
        self._timeline.set_frame_range(0, self.sim_data.data_points - 1)
        self._timeline.frameChanged.connect(self.update_trajectory)

        self._timeline.start()

        # Sync slider with animation
        self._timeline.frameChanged.connect(self.sync_slider_with_animation)

    def camera_mode_change(self, i: int):
        self.camera_mode = i
        self.config.set_value("SIMULATION", "camera_mode", str(i))

    def add_plot(self, parent: QtWidgets.QLayout, title: str, x_label: str, y_label: str, pen: str | list[str], name: str | list[str],
                 legend: bool = True) -> pg.PlotItem | dict:
        """
        Adds a plot to the layout.

        Args:
            parent (QtWidgets.QLayout): parent layout
            title (str): title of the plot
            x_label (str): x-axis label
            y_label (str): y-axis label
            pen (str | list[str]): color or colors of the plots
            name (str | list[str]): name of the plot
            legend (bool): show legend

        Returns:
            pg.PlotItem | dict: plot item or dictionary of plot items
        """

        plot = pg.PlotWidget(title=title)
        parent.addWidget(plot)
        plot.setLabel('bottom', x_label)
        plot.setLabel('left', y_label)
        plot.showGrid(x=True, y=False)

        if legend:
            legend = plot.addLegend()
            legend.anchor((0, 0), (0, 0))

        if isinstance(pen, list) and isinstance(name, list):
            dictionary = {}
            for p, n in zip(pen, name):
                dictionary[n] = plot.plot(pen=p, name=n)
            return dictionary

        return plot.plot(pen=pen, name=name)

    def add_scatter_plot(self, parent: QtWidgets.QLayout, title: str, x_label: str, y_label: str,
                         symbol: str | list[str], color: str | list[str], size: int | list[int],
                         name: str | list[str], x_range: tuple[float, float] = None, y_range: tuple[float, float] = None,
                         legend: bool = True) -> pg.PlotItem | dict:
        """
        Adds a scatter plot to the layout with fixed axis limits.

        Args:
            parent (QtWidgets.QLayout): parent layout
            title (str): title of the plot
            x_label (str): x-axis label
            y_label (str): y-axis label
            symbol (str | list[str]): symbol(s) for the scatter plot
            color (str | list[str]): color(s) of the points
            size (int | list[int]): size(s) of the points
            name (str | list[str]): name of the plot
            x_range (tuple): fixed x-axis range (min, max)
            y_range (tuple): fixed y-axis range (min, max)
            legend (bool): show legend

        Returns:
            pg.PlotItem | dict: scatter plot item or dictionary of scatter plot items
        """

        plot = pg.PlotWidget(title=title)
        parent.addWidget(plot)
        plot.setLabel('bottom', x_label)
        plot.setLabel('left', y_label)
        plot.showGrid(x=True, y=True)

        # Set fixed axis limits
        if x_range is not None and y_range is not None:
            plot.setXRange(*x_range, padding=0)
            plot.setYRange(*y_range, padding=0)
            plot.setMouseEnabled(x=False, y=False)  # Disable panning and zooming

        if legend:
            plot.addLegend()

        scatter = pg.ScatterPlotItem(size=size, pen=pg.mkPen(None), brush=pg.mkBrush(color), symbol=symbol)

        plot.addItem(scatter)
        scatter.setData([], [])  # Initialize empty scatter plot

        return scatter

    @QtCore.pyqtSlot(int)
    def update_trajectory(self, i: int) -> None:
        """
        Updates windows on frame change.
        Args:
            i (int): frame number
        """

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

        self.engine_angle_point.setData([self.sim_data.engine_angle[0][i]], [self.sim_data.engine_angle[1][i]])

        # self.update_camera_position(i)
        match self.camera_mode:
            case 0:
                self.camera_follow(i)
            case 1:
                self.camera_pov(i)
            case 2:
                self.camera_landscape(i)

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

    def camera_follow(self, tick: int) -> None:
        obj_position = np.array(self.sim_data.position_data[tick])
        pos = pg.Vector(*obj_position)
        # distance = self.object.height * 5

        self.view.setCameraPosition(pos=pos)

    def camera_pov(self, tick: int) -> None:
        # TODO
        pass

    def camera_landscape(self, tick: int) -> None:
        # TODO
        pass

    def update_camera_position(self, tick: int) -> None:
        """
        Updates camera position based on the simulation tick.
        Args:
            tick (int): simulation tick
        """

        obj_position = np.array(self.sim_data.position_data[tick])
        obj_position[2] = obj_position[2] / 2
        pos = pg.Vector(*obj_position)

        distance = int(self.camera_distance)
        computed = (obj_position[2]) / math.tan(math.radians(45))
        print(distance, computed)
        if computed > distance:
            distance = computed

        self.view.setCameraPosition(pos=pos, distance=distance)

    def sync_slider_with_animation(self, frame: int) -> None:
        """
        Syncs frame slider with animation.

        Args:
            frame (int): simulation frame
        """

        self.slider.setValue(frame)

    def toggle_pause(self) -> None:
        """
        Toggles pause state of the simulation.
        """

        if self._timeline.paused:
            self._timeline.resume()
            self.pause_button.setText('Pause')
        else:
            self._timeline.pause()
            self.pause_button.setText('Resume')

    def slider_value_changed(self, value: int) -> None:
        """
        Pauses simulation and updates the simulation based on the slider value

        Args:
            value (int): slider value
        """

        self._timeline._counter = value
        self.update_trajectory(value)

    def keyPressEvent(self, event: QKeyEvent):
        """
        Key press event handler.
        Args:
            event (QKeyEvent): key event
        """

        if event.key() == Qt.Key_Space:
            self.toggle_pause()
