import math
from pl.edu.agh.iwum.pendulum.controllers.classifier.Dataset import Dataset
from pl.edu.agh.iwum.pendulum.model.InvertedPendulumModel import InvertedPendulumModel

import random

class DatasetBlindGenerator(object):

    def __init__(self,pendulum_mass, cart_mass,pendulum_length):
        self.pendulum_mass = pendulum_mass
        self.cart_mass=cart_mass
        self.pendulum_length = pendulum_length
        self.model = InvertedPendulumModel(self.pendulum_length,self.pendulum_mass,self.cart_mass)
        mass = cart_mass + pendulum_mass
        self.force = mass*10
        self.radian = 0.0174532925

    def get_force(self):
        return self.force

    def generateRandomDataset(self,tests_number):
        result_dataset = Dataset()
        for i in range(tests_number):
            situations = self._get_random_situations()
            for situation in situations:
                model_response = self._evaluate_model_response(situation)
                result_dataset.add_case(list(situation),model_response)
        return result_dataset

    def _get_random_situations(self):
        angular_position = random.uniform(*self._get_angle_range())
        angular_velocity = random.uniform(*self._get_angular_velocity_range())
        cart_position = random.uniform(*self._get_position_range())
        cart_velocity = random.uniform(*self._get_velocity_range())
        return [(angular_position,angular_velocity,cart_position,cart_velocity, self.force),
                (angular_position,angular_velocity,cart_position,cart_velocity, -self.force)]

    def _evaluate_model_response(self, situation):
        dt = 0.01
        angular_position = situation[0]
        angular_velocity = situation[1]
        cart_position = situation[2]
        cart_velocity = situation[3]
        force = situation[4]
        self.model.set_state(angular_position,angular_velocity,cart_position,cart_velocity)
        self.model.apply(force, dt)
        new_state = self.model.get_state()
        new_angular_position = new_state[0]
        #return self.normalize(new_angular_position)
        return new_angular_position

    def _get_velocity_range(self):
        return [-0.5,0.5]

    def _get_position_range(self):
        return [-20,20]

    def _get_angle_range(self):
        return [-0.785,0.785] #pi/4

    def _get_angular_velocity_range(self):
        return [-3.14,3.14]

    def sign(self,x):
        return 1 if x >= 0 else -1

    def normalize(self, rad):
        return int((rad / self.radian))

    def get_radian(self):
        return self.radian


