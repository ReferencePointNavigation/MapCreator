import os
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'elvis_dock_widget.ui'))


class SelectValue(QtCore.QObject):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.value = value


class ElvisDockWidget(QtWidgets.QDockWidget, FORM_CLASS):

    def __init__(self, elvis, parent=None):
        super().__init__(parent)
        self.elvis = elvis
        self.setupUi(self)
        self.setVisible(False)
        self.visibilityChanged.connect(self.on_visibility_changed)
        self.building_select.activated.connect(self.on_building_select_activated)

    def on_visibility_changed(self, changed):
        self.setVisible(changed)
        if changed:
            self.add_buildings(self.elvis.get_buildings())
        self.simulation_group.setEnabled(True)

    def on_building_select_activated(self, index):
        building = self.building_select.currentData().value
        self.landmark_to_select.clear()
        self.landmark_from_select.clear()
        for floor in building.get_floors():
            self.add_landmarks([l for l in floor.get_landmarks()])

    def add_buildings(self, buildings):
        self.building_select.clear()
        for building in buildings:
            self.building_select.addItem(building.get_name(), userData=SelectValue(building, self))

    def add_landmarks(self, landmarks):
        lm = [l.get_name() for l in landmarks]
        self.landmark_to_select.addItems(lm)
        self.landmark_from_select.addItems(lm)
