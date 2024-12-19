from PhysicsEngine import IObject, IThrust, IAerodependent


class Rocket(IObject, IThrust):
    def __init__(self):
        IObject.__init__(self)
        IThrust.__init__(self, cot=0.1)

    def mass_flow_rate(self, time: float) -> float:
        return 1.2 if time < 10 else 0

    def exhaust_velocity(self, time: float) -> float:
        return 9
