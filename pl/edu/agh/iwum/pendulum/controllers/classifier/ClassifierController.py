from pl.edu.agh.iwum.pendulum.controllers.Controller import Controller
from sklearn import tree

class ClassifierController(Controller):
    def __init__(self, pendulum_mass, cart_mass):
        super.__init__(pendulum_mass,cart_mass)
        self.decisionTree = tree.DecisionTreeClassifier()

    def learn(self, dataset):
        self.decisionTree = self.decisionTree.fit(dataset.data, dataset.target)

    def calculate_force(self, angular_position, angular_velocity, cart_position, cart_velocity):
        return self.decisionTree.predict([angular_position,angular_velocity,cart_position,cart_velocity])