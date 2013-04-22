from pybrain.rl.environments import Environment

class CartEnvironment(Environment):

#TODO implement :P
    def getSensors(self):
        """ the currently visible state of the world (the observation may be
            stochastic - repeated calls returning different values)

            :rtype: by default, this is assumed to be a numpy array of doubles
            :note: This function is abstract and has to be implemented.
        """
        pass

    def performAction(self, action):
        """ perform an action on the world that changes it's internal state (maybe
            stochastically).
            :key action: an action that should be executed in the Environment.
            :type action: by default, this is assumed to be a numpy array of doubles
            :note: This function is abstract and has to be implemented.
        """
        pass

    def reset(self):
        """ Most environments will implement this optional method that allows for
            reinitialization.
        """
        pass