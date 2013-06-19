from time import sleep
from PyQt4.QtGui import QApplication


class Simulation(object):
    def __init__(self, model, controller, sleeping_mode=True):
        self.pendulum_model = model
        self.controller = controller
        self.sleeping_mode = sleeping_mode

    def run(self,speedMultiplier,dt):
        self.running = True
        while self.running:
            for i in range(speedMultiplier):
                self.__step(dt)
            if QApplication.instance() is not None:
                QApplication.instance().processEvents()

    def __step(self, dt):
        F = self.controller.calculate_force(*self.pendulum_model.get_state())
        self.pendulum_model.apply(F, dt)
        if self.sleeping_mode:
            sleep(dt / 2)

    def stop(self):
        self.running = False
