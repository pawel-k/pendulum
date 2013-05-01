from numpy import array
from pybrain.rl.environments import Task

class CartMovingTask(Task):

    def __init__(self,env):
        self.env = env
        self.sensor_limits = None
        self.actor_limits =  None

    def performAction(self, action):
        Task.performAction(self, int(action[0]))

    def getReward(self):
        """ Compute and return the current reward (i.e. corresponding to the last action performed) """
        if self.env.failed():
            self.env.reset()
            return -1
        else:
            return 0

    def getObservation(self):
        return array([self.env.get_current_state()])
