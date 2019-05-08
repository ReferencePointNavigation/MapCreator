import os, zipfile

from referencepoint import MapImporter, MapExporter, MapReader, MapWriter

class MapBuilder:
    """
    The MapBuilder class is the Controller for the plugin
    """
    map = None

    def __init__(self, view, map):
        self.view = view
        self.view.set_controller(self)
        self.map = map

    def new_map(self, name):
        self.map.new_map(name)
        self.view.add_layers(self.map.get_layers().values())

    def import_map(self, file):
        reader = MapReader(self.map, file)
        importer = MapImporter(self.map, reader)
        importer.import_map()

    def save_map(self, filepath):
        writer = MapWriter(self.map.get_name(), filepath)
        exporter = MapExporter(self.map, writer)
        exporter.export_map()
