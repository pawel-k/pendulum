from numpy import *


class InvertedPendulumModel(object):
    def __init__(self, pendulum_length, pendulum_mass, cart_mass):
        self.pendulum_length = pendulum_length
        self.pendulum_mass = pendulum_mass
        self.cart_mass = cart_mass
        self.angular_position = 0.0     # rad
        self.angular_velocity = 0.0     # rad/s
        self.cart_position = 0.0        # m
        self.cart_velocity = 0.0        # m/s
        self.observers = []

    def get_state(self):
        return self.angular_position, self.angular_velocity, self.cart_position, self.cart_velocity

    def set_state(self, angular_position, angular_velocity, cart_position, cart_velocity):
        self.angular_position = self.__normalize_angle(angular_position)
        self.angular_velocity = angular_velocity
        self.cart_position = cart_position
        self.cart_velocity = cart_velocity
        self.__notify_observers()

    def apply(self, F, dt):
        g = 9.80665
        l = self.pendulum_length
        O = self.angular_position
        w = self.angular_velocity
        x = self.cart_position
        v = self.cart_velocity
        so = sin(O)
        co = cos(O)
        m = self.pendulum_mass
        mc = self.cart_mass
        M = m + mc

        q = (g * so + (-F - m * l * w * w * so) * co / M) / (l * (4.0 / 3.0 - m * co * co / M))
        a = (F - (m * l * (w * w * so - q * co))) / M

        self.angular_velocity = w + q * dt
        self.angular_position = self.__normalize_angle(O + self.angular_velocity * dt)
        self.cart_velocity = v + a * dt
        self.cart_position = x + self.cart_velocity * dt

        self.__notify_observers()

    def register_observer(self, observer):
        self.observers.append(observer)

    def __notify_observers(self):
        for observer in self.observers:
            observer.update_state(self.angular_position, self.cart_position)

    def __normalize_angle(self, x):
        angle = (x + pi) % (2 * pi) - pi
        return angle