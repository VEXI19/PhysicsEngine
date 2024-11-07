class Rocket(IObject, IThrust, IGravitational, IAerodependent, ICube):
    def __init__(self, position: list, velocity: list, length:float, width:float, height:float, rotation: list, mass: float, thrust, mass_flow_rate, exhaust_velocity, drag_coefficient: float, lift_coefficient: float, reference_area: float):
        self.position = position
        self.rotation = rotation
        self.velocity = velocity
        self.mass = mass
        self.thrust = thrust
        self.mass_flow_rate = mass_flow_rate
        self.exhaust_velocity = exhaust_velocity
        self.drag_coefficient = drag_coefficient
        self.lift_coefficient = lift_coefficient
        self.reference_area = reference_area
        self.length = length
        self.width = width
        self.height = height

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

    def get_thrust(self) -> float:
        return self.thrust()        

    def get_mass_flow_rate(self) -> float:
        return self.mass_flow_rate()
    
    def get_exhaust_velocity(self) -> float:
        return self.exhaust_velocity()
    
    def get_drag_coefficient(self):
        return self.drag_coefficient

    def get_reference_area(self):
        return self.reference_area
    
    def get_lift_coefficient(self):
        return self.lift_coefficient
    
    def get_length(self) -> float:
        return self.length
    
    def get_width(self) -> float:
        return self.width
    
    def get_height(self) -> float:
        return self.height
        

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

object = Rocket([0, 0, 0], [0, 0, 0], [0, 1, 1], [1, 1, 1], 2, 1, 1, 1, 1, 1, 1, 1, 1)
print(object.get_position())

environment = Environment(1, 1, 1, 1, [0, 0, 0], [0, 0, 0])
print(environment.get_air_density())

physicsEngine = PhysicsEngine(object, environment, 0.01)
print(physicsEngine.drag())
