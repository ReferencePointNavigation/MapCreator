from .map import Map
from .map_importer import MapImporter
from .map_exporter import MapExporter


class MapBuilder:
    """
    The MapBuilder class is the Controller for the plugin
    """
    map = None

    def __init__(self, view, layer_factory):
        self.view = view
        self.view.set_controller(self)
        self.layer_factory = layer_factory

    def import_map(self, file):
        importer = MapImporter(self.map)
        importer.import_map(file)

    def new_map(self, name):
        self.map = Map(name)
        layers = self.layer_factory.new_layers()
        self.map.add_layers(layers)
        self.view.add_layers(layers.values())

    def save_map(self, filepath):
        exporter = MapExporter(self.map)
        exporter.export_map(filepath)
