class DatasetGenerator(object):

    def __init__(self,pendulum_mass, cart_mass):
        self.pendulum_mass = pendulum_mass
        self.cart_mass=cart_mass

    def generateRandomDataset(self,tests_number):
        test_data = []
        actions = []
        for i in range(tests_number):
            #TODO implement :P
            pass