from ..Utils import aero

class PhysicsEngine:
    def __init__(self, object, environment, time_step):
        self.object = object
        self.environment = environment
        self.time_step = time_step
        self.pipeline = []

    def add_force(self, force):
        self.pipeline.append(force)

    def update(self):
        for force in self.pipeline:
            self.object.apply_force(force)
        self.object.update(self.time_step)

    def gravity(self):
        return self.object.get_weight()
    
    @aero
    def drag(self):
        return 20
    
