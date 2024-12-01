from PhysicsEngine import IEnvironment


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
