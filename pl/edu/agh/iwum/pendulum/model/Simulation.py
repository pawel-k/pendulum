from time import sleep
from PyQt4.QtGui import QApplication


class Simulation(object):
    def __init__(self, model, controller):
        self.pendulum_model = model
        self.controller = controller

    def run(self):
        self.running = True
        while self.running:
            self.__step(0.01)
            QApplication.instance().processEvents()

    def __step(self, dt):
        F = self.controller.calculate_force(*self.pendulum_model.get_state())
        self.pendulum_model.apply(F, dt)
        sleep(dt / 2)

    def stop(self):
        self.running = False
