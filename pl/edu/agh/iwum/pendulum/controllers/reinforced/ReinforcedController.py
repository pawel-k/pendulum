from numpy import mean
from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments import EpisodicExperiment
from pybrain.rl.learners import ENAC
from pybrain.tools.shortcuts import buildNetwork
from pl.edu.agh.iwum.pendulum.controllers.Controller import Controller
from pl.edu.agh.iwum.pendulum.controllers.reinforced.CartEnvironment import CartEnvironment
from pl.edu.agh.iwum.pendulum.controllers.reinforced.CartMovingTask import CartMovingTask
from pl.edu.agh.iwum.pendulum.model.InvertedPendulumModel import InvertedPendulumModel

class ReinforcedController(Controller):
    NAME = "Reinforced Controller"

    def __init__(self,pendulum_length,pendulum_mass, cart_mass):
        super(ReinforcedController,self).__init__(pendulum_length,pendulum_mass,cart_mass)
        self.learn(50)

    def learn(self,number_of_iterations):
        learner = ENAC()
        model = InvertedPendulumModel(self.pendulum_length,self.pendulum_mass,self.cart_mass)
        environment = CartEnvironment(model)
        task = CartMovingTask(environment)
        self.controller = buildNetwork(task.outdim, task.indim, bias=False)
        agent = LearningAgent(self.controller, learner)
        experiment = EpisodicExperiment(task, agent)
        for i in range(number_of_iterations):
            experiment.doEpisodes(10)
            reward = mean(agent.history.getSumOverSequences('reward'))
            print i, reward
            agent.learn()
            agent.reset()

    def calculate_force(self, angular_position, angular_velocity, cart_position, cart_velocity):
        force = self.controller.activate([angular_position, angular_velocity, cart_position, cart_velocity])
        return force
