from numpy import array
from pybrain.rl.environments import Task

class CartMovingTask(Task):

    def __init__(self,env,max_steps=10):
        self.env = env
        self.sensor_limits = None
        self.actor_limits =  None
        self.max_steps = max_steps
        self.current_steps = 0

    def performAction(self, action):
        Task.performAction(self, int(action[0]))

    def getReward(self):
        """ Compute and return the current reward (i.e. corresponding to the last action performed) """
        if (self.current_steps > self.max_steps):
            self.env.reset()
            self.current_steps=0
            return 1
        else:
            self.current_steps+=1
            return 0


    def getObservation(self):
        return array([self.env.get_current_state()])
