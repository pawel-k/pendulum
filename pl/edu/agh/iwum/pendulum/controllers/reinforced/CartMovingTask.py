from pybrain.rl.environments import Task

class CartMovingTask(Task):

#TODO implement :P
    def getReward(self):
        """ Compute and return the current reward (i.e. corresponding to the last action performed) """
        return self.env.get_current_state_reward()
