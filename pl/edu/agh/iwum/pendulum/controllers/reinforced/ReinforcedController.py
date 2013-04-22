from pl.edu.agh.iwum.pendulum.controllers.Controller import Controller

class ReinforcedController(Controller):

    def __init__(self, pendulum_mass, cart_mass):
        super.__init__(pendulum_mass,cart_mass)

    def calculate_force(self, angular_position, angular_velocity, cart_position, cart_velocity):
        raise NotImplementedError("Subclass must implement abstract method")
