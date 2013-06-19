from numpy.core.umath import pi

class ExecutionMonitor(object):
    def __init__(self, debug, max_steps, simulation):
        self.steps = 0
        self.degrees = 0
        self.simulation = simulation
        self.debug = debug
        self.max_steps = max_steps

    def update_state(self, angular_position, cart_position):
        degrees = abs(angular_position * 180 / pi)
        self.steps += 1
        self.degrees += degrees
        if self.debug and self.steps % 1000 == 0:
            print self.steps, degrees
        if degrees > 45 or self.steps > self.max_steps:
            self.simulation.stop()

    def results(self):
        return self.steps, self.degrees / self.steps
