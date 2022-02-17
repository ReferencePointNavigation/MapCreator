from ui.qgs_feature import Building, Floor, Room, Landmark, Path
from PyQt5.QtCore import pyqtSignal, QObject


class QgsMap(QObject):

    map_created = pyqtSignal()

    levels_changed = pyqtSignal()

    def __init__(self, name=u"Untitled"):
        super().__init__()
        self.layers = None
        self.name = name
        self.crs = "EPSG:3857"

    def new_map(self, name, layers):
        self.name = name
        self.layers = layers
        self.layers['rooms'].levels_changed.connect(lambda: self.levels_changed.emit())
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