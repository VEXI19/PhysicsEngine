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
env = make_vec_env(lambda: RocketEnv(Rocket, Environment1, reward_function))
env = VecNormalize(env, norm_obs=True, norm_reward=True)

# Train PPO policy
policy_kwargs = dict(net_arch=[32, 64, 64, 64, 32])  # Small network for faster inference
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = PPO('MlpPolicy', env, policy_kwargs=policy_kwargs, device=device)

# # Save model
model_name = "straight_flight"
config = Config()
path = os.path.join(config["SIMULATION"]["simulation_files_folder_path"], "training_1", "models", model_name)
model.save(path)

# Save normalization statistics


