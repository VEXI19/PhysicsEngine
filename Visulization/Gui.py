from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import pandas as pd
from .Timer import TimeLine


class FlightData:
    def __init__(self, file_path):
        print(f"Reading data from file {file_path}")
        self.read_data(file_path)
        print("Data read successfully")

    @property
    def time_step(self):
        return self._time_step

    @property
    def position_data(self):
        return self._positions

    @property
    def velocity_data(self):
        return self._velocities

    @property
    def acceleration_data(self):
        return self._accelerations

    @property
    def starting_position(self):
        return self._starting_position

    @property
    def data_points(self):
        return self._data_points

    def read_data(self, file_path):
        with open(file_path, 'r') as file:
            # reads first line with configuration information
            self._time_step = float(file.readline().strip())

            # reads simulation data
            data = pd.read_csv(file_path, skiprows=1)
            self._positions = np.column_stack([data['pos_x'], data['pos_y'], data['pos_z']])
            self._velocities = np.array([data['vel_x'], data['vel_y'], data['vel_z']])
            self._accelerations = np.array([data['acc_x'], data['acc_y'], data['acc_z']])
            self._data_points = len(self._positions)
            self._starting_position = self._positions[0]



class Gui(QtWidgets.QWidget):
    def __init__(self, file_path: str, camera_distance: int = 50):
        super().__init__()

        # CONFIG
        self.camera_distance = camera_distance

        # WINDOW SETUP
        self.setWindowTitle("Rocket flight visualization")

        # DATA SETUP
        self.sim_data = FlightData(file_path)
        # WIDGETS
        # 3D View
        self.view = gl.GLViewWidget()
        self.view.setCameraPosition(distance=self.camera_distance)  # Adjusted for better view
        grid = gl.GLGridItem()
        grid.setSize(20, 20)
        self.view.addItem(grid)

        # Change color and size of rocket point (make it larger and different color)
        self.rocket_point = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]), color=(1, 0, 0, 1),
                                                 size=10)  # Adjusted size
        self.trajectory_line = gl.GLLinePlotItem(pos=np.array([[0, 0, 0]]), color=(0, 0, 1, 1), width=2)
        self.view.addItem(self.rocket_point)
        self.view.addItem(self.trajectory_line)

        # Overlay Graphics View for displaying text on top of GLViewWidget
        self.overlay_view = QtWidgets.QGraphicsView(self)
        self.overlay_scene = QtWidgets.QGraphicsScene(self.overlay_view)
        self.overlay_view.setScene(self.overlay_scene)
        self.overlay_view.setStyleSheet("background: black; border: none")
        self.overlay_view.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # Adding text to the overlay
        self.text_item = QtWidgets.QGraphicsTextItem("Time: 0.00 s")
        self.text_item.setDefaultTextColor(QtCore.Qt.white)  # Set text color
        # self.text_item.setFont(QtWidgets.QFont("Arial", 16))  # Set font size and style
        self.overlay_scene.addItem(self.text_item)
        self.text_item.setPos(10, 10)  # Top-left corner

        # Layouts
        layout = QtWidgets.QHBoxLayout(self)


        # 2D Plot Layout (for extra graphs)
        graph_layout = QtWidgets.QVBoxLayout()

        text_layout = QtWidgets.QVBoxLayout()
        text_layout.addWidget(self.overlay_view)

        layout.addLayout(text_layout)  # Overlay text

        layout_3d = QtWidgets.QVBoxLayout()
        layout_3d.addWidget(self.view)
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
        self.rocket_point.setData(pos=np.array([self.sim_data.position_data[i]]))  # Update rocket position
        self.trajectory_line.setData(pos=self.sim_data.position_data[:i + 1])  # Update trajectory

        # Update velocity and acceleration graphs
        self.velocity_curve_dict["Velocity X"].setData(self.sim_data.velocity_data[0][:i + 1])
        self.velocity_curve_dict["Velocity Y"].setData(self.sim_data.velocity_data[1][:i + 1])
        self.velocity_curve_dict["Velocity Z"].setData(self.sim_data.velocity_data[2][:i + 1])

        self.acceleration_curve_dict["Acceleration X"].setData(self.sim_data.acceleration_data[0][:i + 1])
        self.acceleration_curve_dict["Acceleration Y"].setData(self.sim_data.acceleration_data[1][:i + 1])
        self.acceleration_curve_dict["Acceleration Z"].setData(self.sim_data.acceleration_data[2][:i + 1])

        self.altitude_curve.setData(self.sim_data.position_data[:i + 1, 2])

        # Update time text
        current_time = i * self.sim_data.time_step
        self.text_item.setPlainText(f"Time: {current_time:.2f} s")

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
