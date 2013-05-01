import pickle
from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments import Experiment
from pybrain.rl.learners import Q, ActionValueTable
from pl.edu.agh.iwum.pendulum.controllers.Controller import Controller
from pl.edu.agh.iwum.pendulum.controllers.reinforced.CartEnvironment import CartEnvironment
from pl.edu.agh.iwum.pendulum.controllers.reinforced.CartMovingTask import CartMovingTask
from pl.edu.agh.iwum.pendulum.model.InvertedPendulumModel import InvertedPendulumModel

class ReinforcedController(Controller):
    NAME = "Reinforced Controller"

    def __init__(self,pendulum_length,pendulum_mass, cart_mass):
        super(ReinforcedController,self).__init__(pendulum_length,pendulum_mass,cart_mass)
        self.ranges = self.get_ranges()
        self.model = InvertedPendulumModel(self.pendulum_length,self.pendulum_mass,self.cart_mass)
        self.force_granularity=2
        self.environment = CartEnvironment(self.model, *self.ranges,force_granularity=self.force_granularity)
        self.learn(1000)
#        self.load()

    def learn(self,number_of_iterations):
        learner = Q(0.2,0.8)
        task = CartMovingTask(self.environment)
        self.controller = ActionValueTable(reduce(lambda x,y: x*y,map(lambda x: len(x),self.ranges)),self.force_granularity)
        self.controller.initialize(1.)
        agent = LearningAgent(self.controller, learner)
        experiment = Experiment(task, agent)
        for i in range(number_of_iterations):
            print i
            experiment.doInteractions(1)
            agent.learn()
            agent.reset()
        with open("test.pcl","w+") as f:
            pickle.dump(self.controller,f)

    def load(self):
        with open("test.pcl", "r+") as f:
            self.controller = pickle.load(f)

    def calculate_force(self, angular_position, angular_velocity, cart_position, cart_velocity):
        state = self.environment.normalized_state((angular_position, angular_velocity, cart_position, cart_velocity))
        action = self.controller.getMaxAction(state)
        force = self.environment.allActions[action]
        return force

    def get_ranges(self):
        cart_position_ranges =[(-1000000000,-2.4),(-2.4, -0.8),(-0.8, 0.8),(0.8, 2.4),(2.4,1000000000)]
        cart_velocity_ranges=[(-1000000000,-0.5),(-0.5, 0.5),(0.5,1000000000)]
        angles_ranges=[(-6.28,-1),(-1,0),(0,1),(1,6.28)]
        angular_velocity_ranges=[(-1000000000,-3.14),(-3.14,3.14),(3.14,1000000000)]
        return (cart_position_ranges,cart_velocity_ranges,angles_ranges,angular_velocity_ranges)
