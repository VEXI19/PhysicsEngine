from PhysicsEngine import IObject, IThrust, IGravitational, IAerodependent


class Rocket(IObject, IThrust, IAerodependent, IGravitational):
    def __init__(self, mass, position=None, rotation=None, velocity=None):
        IObject.__init__(self)
        IThrust.__init__(self)
        IAerodependent.__init__(self)
        IGravitational.__init__(self, mass)

    def mass_flow_rate(self, time) -> float:
        return 1

    def exhaust_velocity(self, time) -> float:
        return 1

    def reference_area(self, alpha: float = None) -> float:
        return 1

    def drag_coefficient(self, alpha: float = None) -> float:
        return 1