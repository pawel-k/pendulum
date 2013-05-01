import random
from pybrain.rl.environments import Environment

class CartEnvironment(Environment):

    def __init__(self,model):
        self.model = model
        self.action = [0.0]
        self.reset()

    def getSensors(self):
        return self.sensors

    def get_angle(self):
        return self.sensors[0]

    def get_angular_velocity(self):
        return self.sensors[1]

    def get_cart_position(self):
        return self.sensors[2]

    def get_card_velocity(self):
        return self.sensors[3]

    def step(self):
        self.sensors = self._evaluate_action(self.action)
        self.angular_position, self.angular_velocity, self.cart_position, self.cart_velocity = self.sensors

    def performAction(self, action):
        self.action=action
        self.step()

    def _evaluate_action(self, action):
        self._set_model()
        dt = 0.1
        self.model.apply(action[0],dt)
        return self.model.get_state()

    def get_current_state_reward(self):
        reward = 1-abs(self.angular_position/3.14)
        return reward

    def reset(self):
        self.angular_position = random.uniform(-3.14,3.14)
        self.angular_velocity = random.uniform(-3.14,3.14)
        self.cart_position = 0
        self.cart_velocity = random.uniform(-1,1)
        self._set_model()
        self.sensors = self.model.get_state()

    def _set_model(self):
        self.model.set_state(self.angular_position, self.angular_velocity, self.cart_position, self.cart_velocity)

    @property
    def indim(self):
        return len(self.action)


    @property
    def outdim(self):
        return len(self.sensors)
