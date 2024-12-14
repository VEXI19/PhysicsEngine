from PhysicsEngine import IObject, IThrust, IAerodependent


class Rocket(IObject, IThrust):
    def __init__(self, mass, length, radius, cot, position=None, rotation=None, velocity=None):
        IObject.__init__(self, mass, length, radius)
        IThrust.__init__(self, cot)
        #IAerodependent.__init__(self)

    def mass_flow_rate(self, time: float) -> float:
        return 1.2 if time < 10 else 0

    def exhaust_velocity(self, time: float) -> float:
        return 9

    # def reference_area(self, alpha: float = None) -> float:
    #     return 1
    #
    # def drag_coefficient(self, alpha: float = None) -> float:
    #     return 1
