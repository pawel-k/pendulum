import math
from pl.edu.agh.iwum.pendulum.controllers.Controller import Controller
from sklearn import tree
from pl.edu.agh.iwum.pendulum.controllers.classifierBlind.DatasetBlindGenerator import DatasetBlindGenerator

class ClassifierRegressionController(Controller):
    NAME = "Classifier Regression Controller"

    def __init__(self,pendulum_length,pendulum_mass, cart_mass):
        Controller.__init__(self,pendulum_length,pendulum_mass,cart_mass)
        self.decisionTree = tree.DecisionTreeRegressor()
        self.dataset_generator = DatasetBlindGenerator(pendulum_mass, cart_mass,pendulum_length)

    def learn(self, number):
        dataset = self.dataset_generator.generateRandomDataset(number)
        self.decisionTree = self.decisionTree.fit(dataset.data, dataset.target)
        with open("test.dot", 'w') as f:
            f = tree.export_graphviz(self.decisionTree, out_file=f)

    def calculate_force(self, angular_position, angular_velocity, cart_position, cart_velocity):
        force = self.dataset_generator.get_force()
        move_left_response = self.decisionTree.predict([angular_position,angular_velocity,cart_position,cart_velocity,-force])[0]
        move_right_response = self.decisionTree.predict([angular_position,angular_velocity,cart_position,cart_velocity,force])[0]
        if self.good_positioning(angular_position):
            return self.return_to_start_point(force,cart_position,cart_velocity)
        else:
            return -force if abs(move_left_response) < abs(move_right_response) else force

    def good_positioning(self, position):
        good_position = 1.5* self.dataset_generator.get_radian()
        return abs(position) <= good_position

    def return_to_start_point(self, force, cart_position,cart_velocity):
        return self.sign(cart_position) * force

    def sign(self,x):
        return 1 if x >= 0 else -1

    def moving_too_fast(self, cart_velocity,force):
        return math.fabs(cart_velocity) > force / 10

    def slow_down(self, cart_velocity, force):
        return -self.sign(cart_velocity)*force
