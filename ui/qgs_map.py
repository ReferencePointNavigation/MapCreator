from .qgs_feature import Building, Floor, Room, Landmark, Path
from PyQt5.QtCore import pyqtSignal, QObject


class QgsMap(QObject):

    map_created = pyqtSignal()

    def __init__(self, name, layer_factory, project):
        super().__init__()
        self.name = name
        self.layer_factory = layer_factory
        self.project = project
        self.layers = None
        self.crs = 3857
        self.basemap = layer_factory.get_base_map()
        self.group = None

    def new_map(self, name):
        self.project.clear()
        self.basemap.show()
        self.group = self.project.layerTreeRoot().insertGroup(0, name)
        self.name = name
        self.layers = self.layer_factory.new_layers()
        for layer in self.layers:
            layer.add_to_group(self.group)
        self.map_created.emit()

    def get_name(self):
        return self.name

    def get_buildings(self, bbox=None):
        if self.layers is None:
            return []

        layer = self.layers['buildings']
        floors_layer = self.layers['rooms']
        lm_layer = self.layers['landmarks']

        buildings = [Building(b, layer.fields) for b in layer.get_features(bbox=bbox)]

        for building in buildings:
            box = building.get_bounding_box()
            floor_nos = floors_layer.get_levels(box)
            floors = [Floor(f, floors_layer) for f in floor_nos]
            building.add_floors(floors)
            for floor in floors:
                query = '"level" = \'{}\''.format(floor.get_number())
                rooms = [Room(r, floors_layer.fields) for r in floors_layer.get_features(query=query, bbox=box)]
                floor.add_rooms(rooms)
                query += ' and "indoor" = \'yes\''
                landmarks = [Landmark(l, lm_layer.fields) for l in lm_layer.get_features(query=query, bbox=box)]
                floor.add_landmarks(landmarks)

        return buildings

    def get_landmarks(self):
        layer = self.layers['landmarks']
        query = '"indoor" = \'no\''
        return [Landmark(f, layer.fields) for f in layer.get_features(query=query)]

    def get_paths(self):
        layer = self.layers['paths']
        return [Path(layer, f) for f in layer.get_features()]

    def get_layers(self):
        return self.layers

    def add_feature(self, layer, fields, geom):
        return self.layers[layer].add_feature(fields, geom)

    def set_crs(self, crs):
        self.crs = crs
        for name, layer in self.layers.items():
            layer.set_crs(crs)

    def get_crs(self):
        return self.crs