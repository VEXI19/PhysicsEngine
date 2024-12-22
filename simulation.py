import os
import pickle
from PhysicsEngine.Config import Config

simulation_name = "StarShip"

config = Config()
path = os.path.join(config["SIMULATION"]["simulation_files_folder_path"], simulation_name, "physics_engine.pkl")

with open(path, "rb") as file:
    physics_engine = pickle.load(file)

physics_engine.start()
