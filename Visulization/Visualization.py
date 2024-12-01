import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import math
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec

matplotlib.use('TkAgg')


class Visualization:
    def __init__(self, file_path: str, replay_speed: float = 1.0):
        self.file_path = file_path
        with open(f"{self.file_path}", "r") as file:
            self.time_step = float(file.readline().strip())

        self.tick_rate = 1000 * self.time_step
        self.replay_speed = self.tick_rate / replay_speed

        self.data = pd.read_csv(self.file_path, skiprows=1)

        self.fig = plt.figure(figsize=(5, 4))
        self.fig.canvas.manager.set_window_title('Rocket Simulation')

        self.gs = GridSpec(4, 7)

        self.ax = self.fig.add_subplot(self.gs[0:4, 0:6], projection='3d')
        self.ax.set_xlim(min(self.data['pos_x']) - 10, max(self.data['pos_x']) + 10)
        self.ax.set_ylim(min(self.data['pos_y']) - 10, max(self.data['pos_y']) + 10)
        self.ax.set_zlim(min(self.data['pos_z']) - 1, max(self.data['pos_z']) + 1)
        self.ax.set_title("Rocket Trajectory")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.grid(True)
        self.point, = self.ax.plot([], [], [], 'bo')
        self.scat, = self.ax.plot([], [], [], 'r-')

        self.ax2 = self.fig.add_subplot(self.gs[0, 6])  # 122 means 1 row, 2 columns, second plot
        self.ax2.set_title("Rocket Mass")
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Mass")
        self.ax2.grid(True)

        self.time = []

        self.ax3 = self.fig.add_subplot(self.gs[1, 6])  # 223 means 2 rows, 2 columns, third plot
        self.ax3.set_title("Rocket Altitude")
        self.ax3.set_xlabel("Time")
        self.ax3.set_ylabel("Altitude")
        self.ax3.grid(True)

    def init_point(self):
        self.point.set_data([], [])
        self.point.set_3d_properties([])

        return self.point,

    def animate_point(self, frame):
        self.point.set_data_3d(
            [self.data['pos_x'][frame]],
            [self.data['pos_y'][frame]],
            [self.data['pos_z'][frame]]
        )

        return self.point,

    def init_scat(self):
        self.scat.set_data([], [])
        self.scat.set_3d_properties([])

        return self.scat,

    def animate_scat(self, frame):
        self.scat.set_data([self.data['pos_x'][:frame]], [self.data['pos_y'][:frame]])
        self.scat.set_3d_properties([self.data['pos_z'][:frame]])

        # self.scat.set_data_3d(
        #     [self.data['pos_x'][:frame]],
        #     [self.data['pos_y'][:frame]],
        #     [self.data['pos_z'][:frame]]
        # )

        return self.scat,

    def plot(self):
        anim_point = FuncAnimation(self.fig,
                      self.animate_point,
                      frames=len(self.data),
                      interval=self.replay_speed,
                      blit=False,
                      init_func=self.init_point)

        # anim_scat = FuncAnimation(self.fig,
        #               self.animate_scat,
        #               frames=len(self.data),
        #               interval=self.replay_speed,
        #               blit=False,
        #               init_func=self.init_scat)

        plt.get_current_fig_manager().window.state("zoomed")
        plt.show()


class Plot:
    def __init__(self):
        plt.ion()
        self.fig = plt.figure(figsize=(16, 9))
        self.fig.canvas.manager.set_window_title('Rocket Simulation')
        self.ax = self.fig.add_subplot(232, projection='3d')
        self.ax.set_title("Rocket Trajectory")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.grid(True)

        self.ax2 = self.fig.add_subplot(233)  # 122 means 1 row, 2 columns, second plot
        self.ax2.set_title("Rocket Mass")
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Mass")
        self.ax2.grid(True)

        self.time = []
        self.rocket_mass = []

        self.ax3 = self.fig.add_subplot(236)  # 223 means 2 rows, 2 columns, third plot
        self.ax3.set_title("Rocket Altitude")
        self.ax3.set_xlabel("Time")
        self.ax3.set_ylabel("Altitude")
        self.ax3.grid(True)

        self.rocket_altitude = []

        self.ax4 = self.fig.add_subplot(231)  # 122 means 1 row, 2 columns, second plot
        self.ax4.axis('off')
        self.text_annotation = self.ax4.text(0.95, 0.95, '', transform=self.ax4.transAxes,
                                             ha='right', va='top', fontsize=12, color='white',
                                             bbox=dict(facecolor='black', alpha=0.5))
        self.ax4.set_title("Rocket Data")

        self.ax5 = self.fig.add_subplot(235)  # 122 means 1 row, 2 columns, second plot
        self.ax5.set_title("Rocket Velocity")
        self.ax5.set_xlabel("Time")
        self.ax5.set_ylabel("Velocity")
        self.ax5.grid(True)

        self.rocket_velocity = []

        self.ax6 = self.fig.add_subplot(234)  # 122 means 1 row, 2 columns, second plot
        self.ax6.set_title("Rocket Acceleration")
        self.ax6.set_xlabel("Time")
        self.ax6.set_ylabel("Acceleration")
        self.ax6.grid(True)

        self.rocket_acceleration = []

    def calculate_vector_magnitude(self, vector):
        vector_magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
        return vector_magnitude

    def plot_rocket(self, rocket):
        self.text_annotation.set_text(
            f'Position: {[round(v, 2) for v in rocket.get_position()]}\n'
            f'Velocity: {[round(v, 2) for v in rocket.get_velocity()]}\n'
            f'Acceleration: {[round(v, 2) for v in rocket.get_acceleration()]}\n'
            f'Rotation: {[round(v, 2) for v in rocket.get_rotation()]}\n'
            f'Mass: {rocket.get_mass()}'
        )
        if rocket.get_velocity()[2] > 0:
            self.ax.scatter(rocket.get_position()[0], rocket.get_position()[1], rocket.get_position()[2], color='red')
        elif rocket.get_velocity()[2] < 0:
            self.ax.scatter(rocket.get_position()[0], rocket.get_position()[1], rocket.get_position()[2], color='blue')
        else:
            self.ax.scatter(rocket.get_position()[0], rocket.get_position()[1], rocket.get_position()[2], color='green')

        # self.time.append(Timer.get_time())
        self.rocket_mass.append(rocket.get_mass())
        self.ax2.plot(self.time, self.rocket_mass, color='blue')

        self.rocket_altitude.append(rocket.get_position()[2])
        self.ax3.plot(self.time, self.rocket_altitude, color='green')

        self.rocket_velocity.append(self.calculate_vector_magnitude(rocket.get_velocity()))
        self.ax5.plot(self.time, self.rocket_velocity, color='red')

        self.rocket_acceleration.append(self.calculate_vector_magnitude(rocket.get_acceleration()))
        self.ax6.plot(self.time, self.rocket_acceleration, color='purple')

        plt.draw()
        plt.pause(0.1)

    def close(self):

        plt.ioff()
        plt.show()
        print("Plot closed")
