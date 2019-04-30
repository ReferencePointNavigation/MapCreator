from .map import Map
from .map_importer import MapImporter

class MapBuilder:
    """
    The MapBuilder class is the Controller for the plugin
    """
    map = None

    def __init__(self, view, filter):
        self.view = view
        self.view.set_controller(self)
        self.filter = filter

    def import_map(self, file):
        importer = MapImporter(self.map)
        importer.import_map(file)

    def new_map(self, name):
        self.map = Map(name)
        self.view.add_layer_group(self.map.name)
        for layer in self.map.layers.values():
            layer.layer = self.view.add_layer(layer.name, layer.to_string())

    def save_map(self, dir):
        pass
