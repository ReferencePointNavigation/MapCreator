from PyQt5.QtCore import QPointF, QRectF, QTimer, QObject, pyqtProperty, QPropertyAnimation, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor
from qgis.gui import QgsMapCanvasItem
from qgis.core import QgsPointXY


class PingLocationMarker(QgsMapCanvasItem):
    """
    Position marker for the current location in the viewer.
    """

    class AniObject(QObject):

        def __init__(self):
            super().__init__()
            self._size = 0
            self.startsize = 0
            self.maxsize = 32

        @pyqtProperty(int)
        def size(self):
            return self._size

        @size.setter
        def size(self, value):
            self._size = value

    def __init__(self, canvas):
        self.canvas = canvas
        self.map_pos = QgsPointXY(0.0, 0.0)
        self.aniobject = PingLocationMarker.AniObject()
        QgsMapCanvasItem.__init__(self, canvas)
        self.anim = QPropertyAnimation(self.aniobject, b"size")
        self.anim.setDuration(1000)
        self.anim.setStartValue(self.aniobject.startsize)
        self.anim.setEndValue(self.aniobject.maxsize)
        self.anim.setLoopCount(-1)
        self.anim.valueChanged.connect(self.value_changed)
        self.anim.start()

    @property
    def size(self):
        return self.aniobject.size

    @property
    def halfsize(self):
        return self.aniobject.maxsize / 2.0

    @property
    def maxsize(self):
        return self.aniobject.maxsize

    def value_changed(self, value):
        self.update()

    def paint(self, painter, xxx, xxx2):
        self.setCenter(self.map_pos)

        rect = QRectF(0 - self.halfsize, 0 - self.halfsize, self.size, self.size)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.green)
        painter.setPen(Qt.green)
        painter.drawEllipse(QPointF(0, 0), self.size, self.size)

    def boundingRect(self):
        return QRectF(-self.halfsize * 2.0, -self.halfsize * 2.0, 2.0 * self.maxsize, 2.0 * self.maxsize)

    def setCenter(self, map_pos):
        self.map_pos = map_pos
        self.setPos(self.toCanvasCoordinates(self.map_pos))

    def updatePosition(self):
        self.setCenter(self.map_pos)