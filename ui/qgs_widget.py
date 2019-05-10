from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import pyqtSlot
from qgis.gui import QgsMapCanvasItem
from qgis.core import QgsCsException, QgsCoordinateTransform, QgsPointXY, qgsDoubleNear, QgsMessageLog
from math import ceil
from PyQt5.QtWidgets import QAction


class QgsWidget(QAction):

    RESOURCE_PATH = ':/plugins/map_builder/resources/'

    registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        QgsWidget.registry[cls.__name__] = cls()

    def __init__(self, iface):
        QAction.__init__(self, iface.mainWindow())
        self.iface = iface
        self.triggered.connect(self.action)

    def get_resource(self, name):
        return self.RESOURCE_PATH + name + '.svg'

    def translate(self, text):
        return text

    def action(self):
        pass


class WidgetFactory:

    def __init__(self, iface):
         self.iface = iface

    def get_widget(self, name):
        pass

    def get_widgets(self):
        return QgsWidget.registry

