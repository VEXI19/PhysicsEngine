from PhysicsEngine import IObject, IThrust, IGravitational, IAerodependent


class Rocket(IObject, IThrust, IGravitational):
    def __init__(self, mass, position=None, rotation=None, velocity=None, acceleration=None):
        IObject.__init__(self, position, rotation, velocity, acceleration)
        IThrust.__init__(self)
        IGravitational.__init__(self, mass)

    def mass_flow_rate(self, time: float) -> float:
        return 1.2 if time < 10 else 0

    def exhaust_velocity(self, time: float) -> float:
        return 9
