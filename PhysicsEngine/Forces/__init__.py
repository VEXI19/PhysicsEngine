from .Gravity import gravity
from .Thrust import thrust
from .Drag import drag
from .Wind import wind
from .Lift import lift


class Forces:
    def __init__(self):
        self.gravity = gravity
        self.thrust = thrust
        self.drag = drag
        self.wind = wind
        self.lift = lift
