from .UIInterface import UIInterface
from PyQt5.QtWidgets import QAction, QActionGroup, QToolButton, QMenu
from PyQt5.QtGui import QIcon
from qgis.core import QgsVectorLayer, QgsProject, QgsFeatureRequest


class LevelMenu(UIInterface):

    def __init__(self, plugin):
        super().__init__(plugin)

        icon = QIcon(self.plugin.resource_path + 'floors.svg')

        self.level_menu = QMenu()
        self.plugin.iface.currentLayerChanged.connect(self.layer_changed)

        self.level_menu_button = QToolButton(self.plugin.iface.mainWindow())
        self.level_menu_button.setMenu(self.level_menu)
        self.level_menu_button.setIcon(icon)
        self.level_menu_button.setPopupMode(QToolButton.InstantPopup)
        self.build_menu()

        self.plugin.toolbar.addWidget(self.level_menu_button)

        self.show_all_action = QAction('Show all', self.plugin.iface.mainWindow())
        self.show_all_action.setCheckable(True)
        self.show_all_action.triggered.connect(lambda b: self.plugin.iface.activeLayer().setSubsetString(None))

        self.level_data = {}

    def layer_changed(self, layer):

        self.level_menu.clear()

        if layer not in self.level_data:
            self.level_menu_button.setEnabled(False)
            return

        self.level_menu_button.setEnabled(True)

        for action in self.level_data[layer].actions():
            self.level_menu.addAction(action)

        self.level_menu.addAction(self.show_all_action)
        self.level_data[layer].addAction(self.show_all_action)

    def build_menu(self):
        layers = [layer for name, layer in QgsProject.instance().mapLayers().items() if type(layer) == QgsVectorLayer]
        for layer in layers:
            layer.setSubsetString(None)
            levels = self.build_level_set(layer)
            group = QActionGroup(self.plugin.iface.mainWindow())
            self.level_data[layer] = group
            for level in levels:
                action = QAction(level, self.plugin.iface.mainWindow())
                action.setCheckable(True)
                action.triggered.connect(lambda b, ly=layer, l=level: self.level_selected(ly, l))
                self.level_menu.addAction(action)
                group.addAction(action)

    def level_selected(self, layer, level):
        layer.setSubsetString(None)
        layer.setSubsetString('"level"=\'{}\''.format(level))
        layer.updateExtents(True)

    def build_level_set(self, layer):
        query = '"level"<> \'NULL\''
        selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        return sorted(set([feature["level"] for feature in selection]))
