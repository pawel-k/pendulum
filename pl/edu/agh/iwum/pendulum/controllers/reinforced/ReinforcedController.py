from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments import Experiment
from pybrain.rl.learners import ActionValueNetwork, Q, ActionValueTable, NFQ
from pl.edu.agh.iwum.pendulum.controllers.Controller import Controller
from pl.edu.agh.iwum.pendulum.controllers.reinforced.CartEnvironment import CartEnvironment
from pl.edu.agh.iwum.pendulum.controllers.reinforced.CartMovingTask import CartMovingTask
from pl.edu.agh.iwum.pendulum.model.InvertedPendulumModel import InvertedPendulumModel

class ReinforcedController(Controller):
    NAME = "Reinforced Controller"

    def __init__(self,pendulum_length,pendulum_mass, cart_mass):
        super(ReinforcedController,self).__init__(pendulum_length,pendulum_mass,cart_mass)
        self.actions_granularity = 10
        self.controller = ActionValueNetwork(4,self.actions_granularity)
        self.learn(50)

    def learn(self,number_of_iterations):
        learner = NFQ()
        model = InvertedPendulumModel(self.pendulum_length,self.pendulum_mass,self.cart_mass)
        agent = LearningAgent(self.controller, learner)
        environment = CartEnvironment(model,self.actions_granularity)
        task = CartMovingTask(environment)
        experiment = Experiment(task, agent)
        for i in range(number_of_iterations):
            experiment.doInteractions(10)
            agent.learn()
            agent.reset()
            print i

    def calculate_force(self, angular_position, angular_velocity, cart_position, cart_velocity):
        return self.controller.getMaxAction([angular_position, angular_velocity, cart_position, cart_velocity])


#def main():
#    pendulum_mass = 0.1
#    cart_mass = 0.5
#    pendulum_length =  0.5
#    actions_granularity = 10
#    number_of_iterations =  1000
#    controller = ActionValueNetwork(4, actions_granularity)
#    learner = NFQ()
#    model = InvertedPendulumModel(pendulum_length,pendulum_mass,cart_mass)
#    agent = LearningAgent(controller, learner)
#    environment = CartEnvironment(model,actions_granularity)
#    task = CartMovingTask(environment)
#    experiment = Experiment(task, agent)
#    while number_of_iterations:
#        experiment.doInteractions(10)
#        agent.learn()
#        agent.reset()
#        print environment.actions[controller.getMaxAction((0,0,0,0))]
#main()