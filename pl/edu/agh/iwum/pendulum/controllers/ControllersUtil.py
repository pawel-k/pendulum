from pl.edu.agh.iwum.pendulum.controllers.RandomController import RandomController
from pl.edu.agh.iwum.pendulum.controllers.classifier.ClassifierController import ClassifierController
from pl.edu.agh.iwum.pendulum.controllers.reinforced.ReinforcedController import ReinforcedController


class ControllersUtil(object):
    RANDOM_CONTROLLER = RandomController.NAME
    REINFORCED_CONTROLLER = ReinforcedController.NAME
    CLASSIFIER_CONTROLLER = ClassifierController.NAME

    REGISTERED_CONTROLLERS = {
        RANDOM_CONTROLLER: RandomController,
        REINFORCED_CONTROLLER: ReinforcedController,
        CLASSIFIER_CONTROLLER: ClassifierController
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