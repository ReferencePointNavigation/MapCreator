from rpn import MapImporter, MapExporter, MapReader, MapWriter, constants
from PyQt5.QtCore import pyqtSignal, QObject
import os


class MapBuilder(QObject):
    """
    The MapBuilder class is the Controller for the plugin
    """
    map_created = pyqtSignal()
    levels_changed = pyqtSignal()

    def __init__(self, map, layer_factory):
        super().__init__()
        self.view = None
        self.layer_factory = layer_factory
        self.map = map
        self.map.map_created.connect(self.on_new_map)
        self.map.levels_changed.connect(self.on_levels_changed)
        self.toolbars = []
        self.views = {}

    def on_new_map(self):
        self.map_created.emit()

    def add_toolbar(self, toolbar):
        self.toolbars.append(toolbar)

    def add_view(self, view_name, view):
        self.views[view_name] = view

    def new_map(self, name):
        self.map.new_map(name, self.layer_factory.new_layers())
        layers = self.map.get_layers()
        basemap = self.layer_factory.get_base_map_layer()
        self.views['layer-view'].new_project(name, layers, basemap)

    def import_map(self, file):
        mapname, _ = os.path.splitext(os.path.basename(file))
        self.new_map(mapname)
        reader = MapReader(self.map, file)
        self.map.set_crs(constants.EPSG_4326)
        importer = MapImporter(self.map, reader)
        importer.import_map()
        self.map.set_crs(constants.EPSG_3857)

    def save_map(self, filepath):
        writer = MapWriter(self.map.get_name(), filepath)
        self.map.set_crs(constants.EPSG_4326)
        exporter = MapExporter(self.map, writer)
        exporter.export_map()
        self.map.set_crs(constants.EPSG_3857)

    def tool_selected(self, tool_name):
        if len(tool_name) > 0:
            self.views['layer-view'].set_active_layer(tool_name)
            self.views['map-view'].add_feature()
        else:
            self.views['map-view'].move_feature()

    def show_minimap(self, enabled):
        self.views['map-view'].show_minimap(enabled)

    def on_levels_changed(self):
        self.levels_changed.emit()

    def get_levels(self):
        return self.map.get_layers()['rooms'].get_levels()

    def set_level(self, level):
        self.map.get_layers()['rooms'].set_level(level)
        self.map.get_layers()['landmarks'].set_level(level)
        self.views['map-view'].set_level(level)