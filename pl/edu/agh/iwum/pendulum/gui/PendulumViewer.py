from __builtin__ import min
from numpy import *

from PyQt4.QtCore import QRectF, QLineF, Qt
from PyQt4.QtGui import QGraphicsScene, QBrush, QPen
from pl.edu.agh.iwum.pendulum.gui.Axis import Axis


class PendulumView(QGraphicsScene):
    def __init__(self, initial_width, initial_height, visible_meters, length, mass):
        QGraphicsScene.__init__(self)
        self.visible_meters = visible_meters
        self.initial_width = initial_width
        self.initial_height = initial_height
        self.pend_radius = min(0.5 * mass, 0.2)
        self.pole_length = length
        self.unit = min(self.initial_width, self.initial_height) / self.visible_meters
        self.__create_scene()
        self.update_state(0.0, 0.0)

    def __create_scene(self):
        # axis
        self.addItem(Axis(self.unit))

        # pendulum
        pendulumPen = QPen(Qt.red, 3)
        pendulumBrush = QBrush(Qt.red)
        self.pole = self.addLine(QLineF(), pendulumPen)
        self.pend = self.addEllipse(QRectF(), pendulumPen, pendulumBrush)

        # reference position
        referencePen = QPen(Qt.black)
        referencePen.setStyle(Qt.DashLine)
        self.reference = self.addLine(QLineF(), referencePen)
        self.reference.setZValue(-1)

        # cart
        self.cart_width = 0.3
        self.cart_height = 0.1
        cartBrush = QBrush(Qt.blue)
        cartPen = QPen(Qt.blue, 5)
        self.cart = self.addRect(QRectF(), cartPen, cartBrush)

    def update_state(self, angular_position, cart_position):
        # pendulum
        pole_xo = self.__translate_x(cart_position)
        pole_yo = self.__translate_y(self.cart_height)
        pole_xi = self.__translate_x(cart_position + self.pole_length * sin(angular_position))
        pole_yi = self.__translate_y(self.cart_height + self.pole_length * cos(angular_position))
        self.pole.setLine(pole_xo, pole_yo, pole_xi, pole_yi)

        # ball
        pend_radius = self.pend_radius * self.unit
        self.pend.setRect(pole_xi - pend_radius, pole_yi - pend_radius, pend_radius * 2, pend_radius * 2)

        # reference position
        reference_line_y = self.__translate_y(self.pole_length * 1.3)
        self.reference.setLine(pole_xo, pole_yo, pole_xo, pole_yo + reference_line_y)

        # cart
        cart_x = self.__translate_x(cart_position - self.cart_width / 2.0)
        cart_y = self.__translate_y(0.)
        cart_width = self.cart_width * self.unit
        cart_height = -self.cart_height * self.unit
        self.cart.setRect(cart_x, cart_y, cart_width, cart_height)

        # move scene
        sceneX = cart_x - self.initial_width / 2
        sceneY = cart_y - self.initial_height / 2
        self.setSceneRect(sceneX, sceneY, self.initial_width, self.initial_height)
        self.update()

    def __translate_x(self, x):
        return int(x * self.unit)

    def __translate_y(self, y):
        return int(-self.unit * y)
