from .Gravity import gravity
from .Thrust import thrust
from .Drag import drag


class Forces:
    def __init__(self):
        self.gravity = gravity
        self.thrust = thrust
        self.drag = drag
