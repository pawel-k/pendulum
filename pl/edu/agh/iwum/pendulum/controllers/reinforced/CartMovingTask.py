from pybrain.rl.environments import Task, EpisodicTask

class CartMovingTask(EpisodicTask):

    def __init__(self,env,max_steps = 100):
        EpisodicTask.__init__(self, env)
        self.N = max_steps
        self.t = 0
        #                    [angular_position,angular_vel,cart_pos,cart_vel]
        self.sensor_limits = [(-3.14,3.14),(-1, 1),(-100.0, +100.0),(-1,1)]
        mass = env.model.pendulum_mass + env.model.cart_mass
        #                    [F]
        self.actor_limits = [(-mass/4, mass/4)]

    def reset(self):
        EpisodicTask.reset(self)
        self.t = 0

    def performAction(self, action):
        self.t+=1
        EpisodicTask.performAction(self, action)

    def isFinished(self):
        if self.t> self.N:
            return True
        return False

    def getReward(self):
        """ Compute and return the current reward (i.e. corresponding to the last action performed) """
        return self.env.get_current_state_reward()
