import math
from pl.edu.agh.iwum.pendulum.controllers.classifier.Dataset import Dataset
from pl.edu.agh.iwum.pendulum.model.InvertedPendulumModel import InvertedPendulumModel

import random

class DatasetGenerator(object):

    def __init__(self,pendulum_mass, cart_mass,pendulum_length):
        self.pendulum_mass = pendulum_mass
        self.cart_mass=cart_mass
        self.pendulum_length = pendulum_length
        self.model = InvertedPendulumModel(self.pendulum_length,self.pendulum_mass,self.cart_mass)
        mass = cart_mass + pendulum_mass
        self.force = mass*10

    def generateRandomDataset(self,tests_number):
        result_dataset = Dataset()
        for i in range(tests_number):
            situation = self._get_random_situation()
            conteract = self._evaluate_model_counteraction(situation)
            result_dataset.add_case(list(situation),conteract)
            print i
        return result_dataset

    def _get_random_situation(self):
        angular_position = random.uniform(*self._get_angle_range())
        angular_velocity = random.uniform(*self._get_angular_velocity_range())
        cart_position = random.uniform(*self._get_position_range())
        cart_velocity = random.uniform(*self._get_velocity_range())
        return angular_position,angular_velocity,cart_position,cart_velocity

    def _evaluate_model_counteraction(self, situation):
        dt = 0.01
        self.model.set_state(*situation)
        self.model.apply(0, dt)
        new_state = self.model.get_state()
        if(new_state[2] > 10):
            return -self.force
        elif(new_state[2] < -10):
            return self.force
        elif(new_state[0]<0.0174532925 and new_state[0]>0) or (new_state[0]>-0.0174532925 and new_state[0]<0):
            return self.sign(new_state[2])*self.force
        elif (new_state[0] > 0):
            return self.force
        else:
            return -self.force

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

