from Configs.Rockets.rocket_1 import Rocket
from Configs.Environments.environment_1 import Environment
from PhysicsEngine import PhysicsEngine, Forces
import numpy as np


rocket = Rocket(1, 2, 0.2, 1)
environment = Environment(1, 1, 20, 1, [1, 1, 1], [1, 1, 1])
physics_engine = PhysicsEngine(rocket, environment, 0.1, file_path="./Simulations/Rocket_2")

physics_engine.add_force(Forces.gravity)
physics_engine.add_force(Forces.thrust)

physics_engine.start()


