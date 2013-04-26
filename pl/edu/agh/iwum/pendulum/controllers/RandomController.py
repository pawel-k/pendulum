import random
from pl.edu.agh.iwum.pendulum.controllers.Controller import Controller


class RandomController(Controller):
    NAME = "Random Controller"

    def __init__(self,pendulum_length, pendulum_mass, cart_mass):
        Controller.__init__(self,pendulum_length, pendulum_mass, cart_mass)

    def calculate_force(self, angular_position, angular_velocity, cart_position, cart_velocity):
        return random.uniform(-1, 1)
