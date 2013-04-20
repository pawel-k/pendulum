from PyQt4.QtCore import Qt, QRectF
from PyQt4.QtGui import QGraphicsItem, QPainter


class Axis(QGraphicsItem):
    def __init__(self, unit):
        QGraphicsItem.__init__(self)
        self.unit = unit
        self.yPosition = unit * 0.03
        self.width = -self.unit * 0.02
        self.lengthInUnits = 200
        self.axisLength = self.lengthInUnits * unit
        self.axisStart = -self.axisLength / 2

    def paint(self, painter, QStyleOptionGraphicsItem, QWidget_widget=None):
        """
        :type painter: QPainter
        """
        painter.setBrush(Qt.black)
        painter.drawRect(self.axisStart, self.yPosition, self.axisLength, self.width)

        for i in range(self.lengthInUnits):
            x = self.axisStart + i * self.unit
            painter.drawLine(x, self.yPosition, x, self.yPosition + 5)
            painter.drawText(QRectF(x - 20, self.yPosition, 40, 20), Qt.AlignCenter, str(i - self.lengthInUnits / 2))


    def boundingRect(self):
        return QRectF(self.axisStart, self.yPosition, self.axisLength, self.width)