from pl.edu.agh.iwum.pendulum.controllers.RandomController import RandomController


class ControllersUtil(object):
    RANDOM_CONTROLLER = RandomController.NAME

    REGISTERED_CONTROLLERS = {
        RANDOM_CONTROLLER: RandomController
    }

    @staticmethod
    def registered_controllers():
        return ControllersUtil.REGISTERED_CONTROLLERS.keys()

    @staticmethod
    def get_controller(name):
        return ControllersUtil.REGISTERED_CONTROLLERS[name]

    @staticmethod
    def default_controller():
        return ControllersUtil.RANDOM_CONTROLLER