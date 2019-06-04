from PyQt5.QtCore import Qt
from ui.qgs_widget import QgsWidget
from .elvis_dock_widget import ElvisDockWidget


class ElvisWidget(QgsWidget):

    registry = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ElvisWidget.registry.append(cls)


class ShowGuiWidget(ElvisWidget):

    def __init__(self, iface, elvis):
        super().__init__(iface, elvis,'elvis', u'Show ELVIS')
        self.elvis = elvis
        self.setEnabled(False)
        self.setCheckable(True)
        self.toggled.connect(self.on_toggled)
        self.dock_widget = ElvisDockWidget(self.elvis)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.dock_widget.show()
        self.controller.map_created.connect(self.map_created)

    def map_created(self):
        self.setEnabled(True)

    def on_toggled(self, checked):
        self.dock_widget.setVisible(checked)