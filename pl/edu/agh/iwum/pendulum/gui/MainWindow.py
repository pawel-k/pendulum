import sys

from PyQt4.QtCore import Qt, pyqtSlot

from PyQt4.QtGui import QMainWindow, QPainter
from numpy.core.umath import pi
from pl.edu.agh.iwum.pendulum.controllers.ControllersUtil import ControllersUtil

from pl.edu.agh.iwum.pendulum.gui.MainWindowUi import Ui_MainWindow

from pl.edu.agh.iwum.pendulum.gui.PendulumViewer import PendulumView
from pl.edu.agh.iwum.pendulum.model.InvertedPendulumModel import InvertedPendulumModel
from pl.edu.agh.iwum.pendulum.model.Simulation import Simulation


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.view.setRenderHint(QPainter.Antialiasing)
        self.__setup_ui()
        self.__create_scene()

    @pyqtSlot()
    def on_run_clicked(self):
        self.__set_widget_state(running=True)
        self.__create_scene()
        self.simulation = Simulation(self.pendulumModel, self.__create_controller())
        self.simulation.run()

    @pyqtSlot()
    def on_stop_clicked(self):
        self.simulation.stop()
        self.__set_widget_state(running=False)

    @pyqtSlot()
    def on_visibility_lostFocus(self):
        self.__create_scene()

    @pyqtSlot()
    def on_pendulumLength_lostFocus(self):
        self.__create_scene()

    @pyqtSlot()
    def on_pendulumMass_lostFocus(self):
        self.__create_scene()

    @pyqtSlot()
    def on_pendulumAngle_lostFocus(self):
        self.__create_scene()

    @pyqtSlot()
    def on_cartPosition_lostFocus(self):
        self.__create_scene()

    def __create_scene(self):
        self.pendulumView = PendulumView(
            self.width(),
            self.height(),
            visible_meters=float(self.ui.visibility.text()),
            length=float(self.ui.pendulumLength.text()),
            mass=float(self.ui.pendulumMass.text())
        )
        self.ui.view.setScene(self.pendulumView)
        self.pendulumModel = InvertedPendulumModel(
            pendulum_length=float(self.ui.pendulumLength.text()),
            pendulum_mass=float(self.ui.pendulumMass.text()),
            cart_mass=float(self.ui.cartMass.text())
        )
        self.pendulumModel.register_observer(self.pendulumView)
        self.pendulumModel.set_state(
            angular_position=float(self.ui.pendulumAngle.text()) * pi / 180.0,
            angular_velocity=float(self.ui.angularVelocity.text()),
            cart_position=float(self.ui.cartPosition.text()),
            cart_velocity=float(self.ui.cartSpeed.text())
        )

    def __create_controller(self):
        return ControllersUtil.get_controller(str(self.ui.controller.currentText()))(
            float(self.ui.pendulumLength.text()),
            float(self.ui.pendulumMass.text()),
            float(self.ui.cartMass.text())
        )

    def __set_widget_state(self, running):
        self.ui.allSettings.setEnabled(not running)
        self.ui.stop.setEnabled(running)
        self.ui.run.setEnabled(not running)

    def __setup_ui(self):
        self.ui.controller.addItems(ControllersUtil.registered_controllers())
        self.ui.controller.setCurrentIndex(self.ui.controller.findText(ControllersUtil.default_controller()))

    def resizeEvent(self, QResizeEvent):
        self.ui.view.fitInView(self.pendulumView.sceneRect(), Qt.KeepAspectRatio)

    def show(self):
        QMainWindow.show(self)
        self.resizeEvent(None)

    def closeEvent(self, QCloseEvent):
        sys.exit(0)