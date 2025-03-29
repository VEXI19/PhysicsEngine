import math
import os

import numpy as np
import progressbar

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecNormalize

from PhysicsEngine.Config import Config
from PhysicsEngine.Utils.EulerAngles import euler_to_rotation_matrix
from SteeringAlgorithm.Wrapper import RocketEnv
import torch

from Configs.Rockets.training_1 import Rocket
from Configs.Environments.no_wind import Environment1

# def reward_function(obj):
#     pitch, yaw, _ = obj.rotation
#     x, y, z = obj.position
#
#     pitch = abs(pitch)
#     yaw = abs(yaw)
#
#     distance_from_z = math.sqrt(x ** 2 + y ** 2)
#
#     rot_matrix = euler_to_rotation_matrix(obj.rotation)
#     local_z = np.array([0, 0, 1])
#     rotated_z = rot_matrix @ local_z
#
#     world_z = np.array([0, 0, 1])
#     cos_theta = np.dot(rotated_z, world_z) / (np.linalg.norm(rotated_z) * np.linalg.norm(world_z))
#     angle = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))
#
#
#
#     # return obj.position[2] - np.linalg.norm(obj.angular_velocity) - np.linalg.norm(obj.acceleration[:2])
#     return -math.sqrt(math.pow(pitch, 2) + math.pow(yaw, 2)) + 5

def reward_function(obj):
    pitch, yaw, _ = obj.rotation
    x, y, z = obj.position

    distance_from_z = math.sqrt(x ** 2 + y ** 2)

    rot_matrix = euler_to_rotation_matrix(obj.rotation)
    local_z = np.array([z, 0, 1])
    rotated_z = rot_matrix @ local_z

    world_z = np.array([0, 0, 1])
    cos_theta = np.dot(rotated_z, world_z) / (np.linalg.norm(rotated_z) * np.linalg.norm(world_z))
    angle = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))

    rotated_z_xy = np.array([rotated_z[0], rotated_z[1], 0])

    position_xy = np.array([x, y, 0])

    dot_product = np.dot(rotated_z_xy, position_xy)

    if dot_product < 0:
        angle = -angle

    return angle

# Wrap environment in VecEnv for PPO
env = make_vec_env(lambda: RocketEnv(Rocket, Environment1, reward_function))
env = VecNormalize(env, norm_obs=True, norm_reward=True)

model_name = "straight_flight"
config = Config()
path = os.path.join(config["SIMULATION"]["simulation_files_folder_path"], "training_1", "models", model_name)
model = PPO.load(path)

model.set_env(env)
total_timesteps = 150000

# Create progress bar
progress = progressbar.ProgressBar(
    max_value=total_timesteps,
    widgets=[
        "Training: ", progressbar.Percentage(), " ",
        progressbar.Bar(), " ",
        progressbar.ETA()
    ]
).start()
current_progress = 0
# Callback function to update progress bar
def progress_callback(_locals, _globals):
    global current_progress
    current_progress += 1
    progress.update(min(current_progress, total_timesteps))
    return True  # Continue training

# Train with progress bar
model.learn(total_timesteps=total_timesteps, callback=progress_callback)

# Finish progress bar
progress.finish()

# # Save model
model_name = "straight_flight"
config = Config()
path = os.path.join(config["SIMULATION"]["simulation_files_folder_path"], "training_1", "models", model_name)
model.save(path)

