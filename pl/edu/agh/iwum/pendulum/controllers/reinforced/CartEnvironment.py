import random
from pybrain.rl.environments import Environment

class CartEnvironment(Environment):

    def __init__(self,model,cart_position_ranges,car_velocity_ranges,angles_ranges,angular_velocity_ranges,force_granularity):
        self.model = model
        self.reset()
        mass = model.cart_mass + model.pendulum_mass
        mass*=10
        self.allActions = [-mass/i for i in range(1,force_granularity)]+[mass/i for i in range(1,force_granularity)]
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

    def failed(self):
        return (abs(self.angular_position) > 0.21) or (abs(self.cart_position) > 3)

    def reset(self):
        self.angular_position = 0#random.uniform(-2,2)
        self.angular_velocity = 0#random.uniform(-4,4)
        self.cart_position = 0#random.uniform(-5,5)
        self.cart_velocity = 0#random.uniform(-1,1)
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

