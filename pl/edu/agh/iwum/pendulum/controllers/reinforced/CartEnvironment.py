import random
from pybrain.rl.environments import Environment

class CartEnvironment(Environment):

    def __init__(self,model,cart_position_ranges,car_velocity_ranges,angles_ranges,angular_velocity_ranges):
        self.model = model
        self.reset()
        mass = model.cart_mass + model.pendulum_mass
        mass*=10
        self.allActions = [-mass/i for i in range(1,11)]+[mass/i for i in range(1,11)]
        self.cart_position_ranges = cart_position_ranges
        self.cart_velocity_ranges = car_velocity_ranges
        self.angles_ranges = angles_ranges
        self.angular_velocity_ranges = angular_velocity_ranges

    def getSensors(self):
        possible_states = []
        for action in self.allActions:
            possible_states.append(self.normalized_state(self._evaluate_action(action)))
        return list(set(possible_states))

    def performAction(self, action):
        self.angular_position, self.angular_velocity, self.cart_position, self.cart_velocity = self._evaluate_action(self.allActions[action])
        self._set_model()

    def _evaluate_action(self, action):
        self._set_model()
        dt = 0.01
        self.model.apply(action,dt)
        return self.model.get_state()

    def get_current_state_reward(self):
        if (self.angular_position < 0.1) and (self.angular_position > -0.1):# and (self.cart_position < 0.24) and (self.cart_position > -0.24) and (abs(self.angular_velocity) < 3.14):
            return 1
        else:
            return 0
#        reward = (1-abs(self.angular_position/3.14)) #* (abs(self.cart_position)-2.41)
#        return reward

    def reset(self):
        self.angular_position = random.uniform(-1,1)
        self.angular_velocity = random.uniform(-4,4)
        self.cart_position = 0
        self.cart_velocity = random.uniform(-1,1)
        self._set_model()
        self.sensors = self.model.get_state()

    def _set_model(self):
        self.model.set_state(self.angular_position, self.angular_velocity, self.cart_position, self.cart_velocity)

    def get_current_state(self):
        return self.normalized_state(self.model.get_state())

    def normalized_state(self, (angular_position, angular_velocity, cart_position, cart_velocity)):
        angle_state = self._get_discrete_state(self.angles_ranges,angular_position)
        angular_vel_state = self._get_discrete_state(self.angular_velocity_ranges,angular_velocity)
        cart_velocity_state = self._get_discrete_state(self.cart_velocity_ranges,cart_velocity)
        cart_position_state = self._get_discrete_state(self.cart_position_ranges,cart_position)
        return \
            angle_state*(len(self.angular_velocity_ranges)*len(self.cart_velocity_ranges)*len(self.cart_position_ranges))+ angular_vel_state*(len(self.cart_velocity_ranges)*len(self.cart_position_ranges))+ cart_velocity_state *len(self.cart_position_ranges) + cart_position_state

    def _get_discrete_state(self,ranges,value):
        for i,position in enumerate(ranges):
            if (value > position[0]) and (value < position[1]):
                return i
        return 0

