import datetime

import gymnasium as gym
import numpy as np
from PhysicsEngine import PhysicsEngine, Forces

class RocketEnv(gym.Env):
    def __init__(self, Rocket, Environment, reward_function, save_data: bool = False):
        super(RocketEnv, self).__init__()

        self.rocket = Rocket
        self.environment = Environment
        self.reward_function = reward_function

        self.save_data = save_data

        self.simulation_count = 0
        self.simulation_tick = 0
        self.engine = None

        self.file_name = f"learning_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        self.reset()
        if self.save_data and self.engine is not None:
            self.engine.file_name = self.file_name
            self.engine.save_data(self.engine.get_config_data())
            self.engine.save_data(self.engine.object.get_data_header())
            self.engine.save_data(
                f"{self.engine.simulation_tick},{self.engine.simulation_time},{self.engine.object.get_data()}")
        self.action_space = gym.spaces.Box(low=-np.radians(20), high=np.radians(20), shape=(2,), dtype=np.float32)  # TVC deflection angles
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32)  # 7 inputs


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.simulation_count += 1
        if self.save_data and self.engine is not None:
            self.engine.save_data(f"{self.engine.simulation_tick},{self.engine.simulation_time},{self.engine.object.get_data()}")
        self.engine = PhysicsEngine(self.rocket(), self.environment(), 0.1, file_name=self.file_name)

        self.engine.add_force(Forces.gravity)
        self.engine.add_force(Forces.thrust)
        self.engine.add_force(Forces.drag)
        self.engine.add_force(Forces.lift)

        obs = self._get_obs()
        return obs, {}

    def step(self, action):
        # if self.simulation_count > self.max_simulations:
        #     return self._get_obs(), 0, True, False, {}
        # Apply thrust vector control (TVC) deflection
        self.engine.object.engine_angle = np.array([action[0], action[1], .0])
        self.simulation_tick += 1

        # Run one tick of the simulation
        resulting_force, resulting_torque = self.engine.compute_force()
        self.engine.compute_change(resulting_force, resulting_torque)
        self.engine.next_tick()
        if self.save_data:
            self.engine.save_data(f"{self.engine.simulation_tick},{self.engine.simulation_time},{self.engine.object.get_data()}")

        # Get observation, reward, and done flag
        obs = self._get_obs()
        reward = self._calculate_reward()

        terminated = self.engine.object.position[2] < 0 or self.engine.simulation_time >= self.engine.max_simulation_time or self.engine.object.mass_flow_rate(self.engine.simulation_time) <= 0 or np.linalg.norm(self.engine.object.velocity) > 4000
        truncated = self.engine.simulation_time >= self.engine.max_simulation_time

        return obs, reward, terminated, truncated, {}

    def _get_obs(self):
        obj = self.engine.object
        return np.concatenate((obj.acceleration, obj.angular_velocity, [obj.position[2]]))  # Accel (x,y,z), Ang vel (x,y,z), height

    def _calculate_reward(self):
        obj = self.engine.object
        # Reward for maintaining upright position and gaining altitude
        return self.reward_function(obj)
