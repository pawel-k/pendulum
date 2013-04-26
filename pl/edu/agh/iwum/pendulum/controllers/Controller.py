class Controller(object):
    def __init__(self,pendulum_length, pendulum_mass, cart_mass):
        self.pendulum_mass = pendulum_mass
        self.cart_mass = cart_mass
        self.pendulum_length = pendulum_length

    def calculate_force(self, angular_position, angular_velocity, cart_position, cart_velocity):
        raise NotImplementedError("Subclass must implement abstract method")