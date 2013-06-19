from pl.edu.agh.iwum.pendulum.controllers.ControllersUtil import ControllersUtil
from pl.edu.agh.iwum.pendulum.model.InvertedPendulumModel import InvertedPendulumModel
from pl.edu.agh.iwum.pendulum.model.Simulation import Simulation
from pl.edu.agh.iwum.pendulum.tester.ExecutionMonitor import ExecutionMonitor

CART_MASS = 1  # kg
PENDULUM_LENGTH = 1  # m
PENDULUM_MASS = 0.1  # m
ANGULAR_VELOCITY = 0
CART_POSITION = 0
CART_VELOCITY = 0

class ConsoleRunner(object):
    def __init__(self, debug, max_steps, name, angular_position):
        self.set_pendulum_model(angular_position)
        self.simulation = Simulation(
            self.pendulumModel,
            self.__create_controller(name),
            sleeping_mode=False
        )
        self.observer = ExecutionMonitor(debug, max_steps, self.simulation)
        self.pendulumModel.register_observer(self.observer)

    def learn(self, iterations):
        self.simulation.controller.learn(iterations)

    def run(self, speed_multiplier, dt):
        self.simulation.run(speed_multiplier, dt)

    def set_pendulum_model(self, angular_position):
        self.pendulumModel = InvertedPendulumModel(
            pendulum_length=PENDULUM_LENGTH,
            pendulum_mass=PENDULUM_MASS,
            cart_mass=CART_MASS
        )
        self.pendulumModel.set_state(
            angular_position=angular_position,
            angular_velocity=ANGULAR_VELOCITY,
            cart_position=CART_POSITION,
            cart_velocity=CART_VELOCITY
        )

    def __create_controller(self, name):
        return ControllersUtil.get_controller(name)(
            PENDULUM_LENGTH,
            PENDULUM_MASS,
            CART_MASS
        )

    def results(self):
        return self.observer.results()
