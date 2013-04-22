from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments import Experiment
from pybrain.rl.learners import ActionValueNetwork, Q
from pl.edu.agh.iwum.pendulum.controllers.Controller import Controller
from pl.edu.agh.iwum.pendulum.controllers.reinforced.CartEnvironment import CartEnvironment
from pl.edu.agh.iwum.pendulum.controllers.reinforced.CartMovingTask import CartMovingTask

class ReinforcedController(Controller):

    def __init__(self, pendulum_mass, cart_mass):
        super.__init__(pendulum_mass,cart_mass)
        self.controller = ActionValueNetwork(4,2)
        self.controller.initialize(1.)

    def learn(self,number_of_iterations):
        learner = Q()
        agent = LearningAgent(self.controller, learner)
        environment = CartEnvironment()
        task = CartMovingTask(environment)
        experiment = Experiment(task, agent)
        while number_of_iterations:
            experiment.doInteractions(10)
            agent.learn()
            agent.reset()

    def calculate_force(self, angular_position, angular_velocity, cart_position, cart_velocity):
        return self.controller.getMaxAction([angular_position, angular_velocity, cart_position, cart_velocity])
