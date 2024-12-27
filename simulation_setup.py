import os


from Configs.Rockets.test_rocket import Rocket
from Configs.Environments.test_env import Environment1 as Environment
from PhysicsEngine import PhysicsEngine, Forces
import pickle

from PhysicsEngine.Config import Config


def save(instance, path, file_name):
    if not os.path.exists(path):
        os.makedirs(path)

    path = os.path.join(path, file_name)

    with open(path, "wb") as file:
        pickle.dump(instance, file)


object = Rocket()

environment = Environment()
physics_engine = PhysicsEngine(object, environment, 0.1)

physics_engine.add_force(Forces.gravity)
physics_engine.add_force(Forces.thrust)
physics_engine.add_force(Forces.drag)
physics_engine.add_force(Forces.wind)
physics_engine.add_force(Forces.lift)

config = Config()
path = os.path.join(config["SIMULATION"]["simulation_files_folder_path"], object.name)

# HAS TO BE OBJ
# object_model_path = "./rocket.obj"
#
# shutil.copyfile(object_model_path, os.path.join(path, "object.obj"))

# save(object, path, "object.pkl")
# save(environment, path, "environment.pkl")
save(physics_engine, path, "physics_engine.pkl")
