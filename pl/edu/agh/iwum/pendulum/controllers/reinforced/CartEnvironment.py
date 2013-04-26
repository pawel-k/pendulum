from collections import namedtuple
from numpy.random import random
from pybrain.rl.environments import Environment

class CartEnvironment(Environment):

    def __init__(self,model,actions_granurality):
        self.model = model
        self.actions_granurality = actions_granurality
        self.actions = self.create_actions()
        self.reset()

    def getSensors(self):
        return self.model.get_state()

    def performAction(self, action):
        self._set_model()
        action_to_execute = self.actions[int(action[0])]
        self.model.apply(action_to_execute[0], action_to_execute[1])
        self.angular_position,self.angular_velocity,self.cart_position,self.cart_velocity = self.model.get_state()

    def get_current_state_reward(self):
        reward = 1-abs(self.angular_position/3.14)
        return reward

    def reset(self):
        self.angular_position = random()
        self.angular_velocity = random()
        self.cart_position = random()
        self.cart_velocity = random()
        self._set_model()

    def _set_model(self):
        self.model.set_state(self.angular_position, self.angular_velocity, self.cart_position, self.cart_velocity)

    def create_actions(self):
        actions = []
        dt = 0.01
        mass = self.model.pendulum_mass + self.model.cart_mass
        F = -mass
        step = (2*mass) / self.actions_granurality
        for i in range(self.actions_granurality):
            action = F,dt
            actions.append(action)
            F+=step
        return actions
