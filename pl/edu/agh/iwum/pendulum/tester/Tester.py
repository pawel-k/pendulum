import os
from os import mkdir
import sys

from numpy.core.umath import pi

from pl.edu.agh.iwum.pendulum.controllers.ControllersUtil import ControllersUtil
from pl.edu.agh.iwum.pendulum.tester.ConsoleRunner import ConsoleRunner


def learn_and_test(controller_name, learning_steps, angle):
    runner = ConsoleRunner(debug=DEBUG, max_steps=MAX_STEPS, name=controller_name,
                           angular_position=(angle * pi) / 180.0)
    runner.learn(learning_steps)
    runner.run(1, 0.01)
    return runner.results()


def run_tests(controller_name, learning_steps, angle):
    total_steps = 0
    total_angle = 0
    if DEBUG:
        print "################################ learning steps: ", str(learning_steps) + ", angle: " + str(
            angle), "################################"
    for i in range(TRIALS):
        if DEBUG:
            print "----------------- iteration ", str(i), "-----------------"
        steps, degrees = learn_and_test(controller_name, learning_steps, angle)
        if DEBUG:
            print "successful steps: ", str(steps)
            print "average pendulum angle: ", str(degrees)
            print "------------------------------------------------------"
        total_steps += steps
        total_angle += degrees
    return total_steps / TRIALS, total_angle / TRIALS


def experiment(controller_name):
    if DEBUG:
        print "====================================== learning ", controller_name + "======================================"
    if not os.path.isdir(results_dir(controller_name)):
        mkdir(results_dir(controller_name))
        mkdir(steps_dir(controller_name))
        mkdir(angles_dir(controller_name))
    for angle in ANGLES:
        steps_file = open_result_file(steps_dir(controller_name), angle)
        average_angle_file = open_result_file(angles_dir(controller_name), angle)
        for learning_steps in LEARNING_STEPS:
            average_steps, average_angle = run_tests(controller_name, learning_steps, angle)
            print "average steps: ", str(average_steps)
            print "average angle: ", str(average_angle)
            steps_file.write(str(learning_steps) + " " + str(average_steps) + "\n")
            average_angle_file.write(str(learning_steps) + " " + str(average_angle) + "\n")


def results_dir(controller_name):
    results_path = os.path.join(RESULTS_PATH, controller_name.translate(None, " "))
    return results_path


def steps_dir(controller_name):
    return os.path.join(results_dir(controller_name), "steps")


def angles_dir(controller_name):
    return os.path.join(results_dir(controller_name), "angles")


def open_result_file(result_dir, angle):
    return open(os.path.join(result_dir, "initial_angle_" + str(angle)), 'w')


MAX_STEPS = 200000
TRIALS = 5
LEARNING_STEPS = [10, 100, 1000, 2000, 5000, 10000, 20000]
ANGLES = [1, 5, 10, 15, 30]
DEBUG = True

RESULTS_PATH = sys.argv[1]


def main():
    if not os.path.isdir(RESULTS_PATH):
        mkdir(RESULTS_PATH)
    for controller in ControllersUtil.REGISTERED_CONTROLLERS:
        experiment(controller)


main()