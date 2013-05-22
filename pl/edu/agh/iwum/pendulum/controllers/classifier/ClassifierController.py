from pl.edu.agh.iwum.pendulum.controllers.Controller import Controller
from sklearn import tree
from pl.edu.agh.iwum.pendulum.controllers.classifier.DatasetGenerator import DatasetGenerator
import StringIO, pydot

class ClassifierController(Controller):
    NAME = "Classifier Controller"

    def __init__(self,pendulum_length,pendulum_mass, cart_mass):
        Controller.__init__(self,pendulum_length,pendulum_mass,cart_mass)
        self.decisionTree = tree.DecisionTreeClassifier()
        dataset_generator = DatasetGenerator(pendulum_mass, cart_mass,pendulum_length)
        self.learn(dataset_generator.generateRandomDataset(10000))

    def learn(self, dataset):
        self.decisionTree = self.decisionTree.fit(dataset.data, dataset.target)
        with open("test.dot", 'w') as f:
            f = tree.export_graphviz(self.decisionTree, out_file=f)


    def calculate_force(self, angular_position, angular_velocity, cart_position, cart_velocity):
        force = self.decisionTree.predict([angular_position,angular_velocity,cart_position,cart_velocity])[0]
        return force