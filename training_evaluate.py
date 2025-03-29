import os

import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecNormalize

from PhysicsEngine.Config import Config
from SteeringAlgorithm.Wrapper import RocketEnv
import torch

from Configs.Rockets.training_1 import Rocket
from Configs.Environments.no_wind import Environment1

def reward_function(obj):
    return obj.position[2] - np.linalg.norm(obj.angular_velocity) - np.linalg.norm(obj.acceleration[:2])

# Wrap environment in VecEnv for PPO
env = make_vec_env(lambda: RocketEnv(Rocket, Environment1, reward_function, True))
env = VecNormalize(env, norm_obs=True, norm_reward=True)

model_name = "straight_flight"
config = Config()
path = os.path.join(config["SIMULATION"]["simulation_files_folder_path"], "training_1", "models", model_name)
model = PPO.load(path)

model.set_env(env)

obs = env.reset()
done = False
while not done:
    action, _states = model.predict(obs)
    obs, reward, done, _ = env.step(action)
