from .protobuf import *

from qgis.core import QgsProject, QgsVectorLayer

building_query = '"building" = \'yes\' and "name" <> \'NULL\''
floor_query = '"indoor"<> \'NULL\''
epsg = "3857"

base_fields = [
    'name:string(25)',
    'level:integer',
    'indoor:string(25)',
]

point_fields = base_fields + [
    'type:string(12)',
    'wheelchair:string(25)',
    'amenity:string(25)',
    'access:string(25)'
]


class Map:
    def __init__(self, name):
        self.name = name
        self.layers = {}
        root = QgsProject.instance().layerTreeRoot()
        self.group = root.insertGroup(0, name)

    def add_layer(self, layer):
        self.layers += {layer.name : layer}
        layer = QgsVectorLayer(layer.to_string(), layer.name, "memory")
        self.group.addLayer(layer)
        return layer

    def export(self, filename):
        pass

    @staticmethod
    def import_from_file(filename):
        pass
