from src import IObject, IGravitational, IEnvironment, PhysicsEngine


class Apple(IObject, IGravitational):
    def __init__(self, position: list, velocity: list, rotation: list, mass: float):
        self.position = position
        self.rotation = rotation
        self.velocity = velocity
        self.mass = mass

    def get_position(self) -> list:
        return self.position

    def get_velocity(self) -> list:
        return self.velocity

    def get_rotation(self) -> list:
        return self.rotation

    def get_mass(self) -> float:
        return self.mass

    def get_weight(self):
        return self.mass * 9.81


class Environment(IEnvironment):
    def __init__(self, air_density, speed_of_sound, temperature, pressure, wind, wind_gradient):
        self.air_density = air_density
        self.speed_of_sound = speed_of_sound
        self.temperature = temperature
        self.pressure = pressure
        self.wind = wind
        self.wind_gradient = wind_gradient

    def get_air_density(self, position=None) -> float:
        return self.air_density

    def get_speed_of_sound(self, position=None) -> float:
        return self.speed_of_sound

    def get_temperature(self, position=None) -> float:
        return self.temperature

    def get_pressure(self, position=None) -> float:
        return self.pressure

    def get_wind(self, position=None) -> list:
        return self.wind

    def get_wind_gradient(self, position=None) -> list:
        return self.wind_gradient


object = Apple([0, 0, 0], [0, 0, 0], [0, 1, 1], 2)
print(object.get_position())

environment = Environment(1, 1, 1, 1, [0, 0, 0], [0, 0, 0])

physicsEngine = PhysicsEngine(object, environment, 0.01)

def add(x, y):
    return x + y

def test_add():
    assert add(1, 2) == 3

