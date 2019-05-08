import os, zipfile

from .map_importer import MapImporter
from .map_exporter import MapExporter


class MapBuilder:
    """
    The MapBuilder class is the Controller for the plugin
    """
    map = None

    def __init__(self, view, map):
        self.view = view
        self.view.set_controller(self)
        self.map = map

    def import_map(self, file):

        zf = zipfile.ZipFile(file)
        f, _ = os.path.splitext(os.path.basename(file))

        data = zf.read(f + '.map')


        importer = MapImporter(self.map)
        importer.import_map(file)

    def new_map(self, name):
        self.map.new_map(name)
        self.view.add_layers(self.map.get_layers().values())

    def save_map(self, filepath):
        exporter = MapExporter(self.map)

        files = exporter.export_map(filepath)

        filename = os.path.join(filepath, self.map.get_name().replace(' ', '_'))
        zf = zipfile.ZipFile(filename + '.rpn', mode='w')

        zf.writestr(filename + '.map', files[0].SerializeToString())

        for building in files[1]:
            zf.writestr(building.name.replace(' ', '_') + '.bldg', building.SerializeToString())

        zf.close()
