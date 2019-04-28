from mapbuilder.protobuf import *

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


    def createNewMap(self, name):

        root = QgsProject.instance().layerTreeRoot()
        self.group = root.insertGroup(0, name)

        self.layers = {
            "point": self.createLayer('Landmarks', epsg, 'Point', point_fields),
            "polygon": self.createLayer('Buildings', epsg, 'Polygon', base_fields),
            "line": self.createLayer('Paths', epsg, 'Line', base_fields)
        }

        for layer in self.layers.values():
            self.group.addLayer(layer)

    def createLayer(self, name, espg, geomType, fields):
        lyrStr = '{0}?crs={0}&field={1}'.format(geomType, epsg, '&field='.join(fields))
        return QgsVectorLayer(lyrStr, name, "memory")


    def export(self, filename):
        pass

    @staticmethod
    def import_from_file(filename):
        pass
