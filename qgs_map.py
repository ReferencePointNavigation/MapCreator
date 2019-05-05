from .qgs_feature import Building, Floor, Room, Landmark, Path

from qgis.core import (
    QgsMessageLog,
    Qgis
)


class QgsMap:

    def __init__(self, name, layer_factory):
        self.__name = name
        self.__layer_factory = layer_factory
        self.__layers = None

    def new_map(self, name):
        self.__name = name
        self.__layers = self.__layer_factory.new_layers()

    def get_name(self):
        return self.__name

    def get_buildings(self):
        layer = self.__layers['buildings']
        buildings = [Building(layer, b) for b in layer.get_features()]
        for building in buildings:
            floors_layer = self.__layers['rooms']
            bbox = building.get_bounding_box()
            floor_nos = sorted(set([f['level'] for f in floors_layer.get_features(bbox=bbox)]))
            floors = [Floor(f) for f in floor_nos]
            building.add_floors(floors)
            for floor in floors:
                query = '"level" = {}'.format(floor.get_number())
                rooms = [Room(floors_layer, r) for r in floors_layer.get_features(bbox=bbox)]
                floor.add_rooms(rooms)
                llayer = self.__layers['landmarks']
                query += ' and "indoor" = \'yes\''
                landmarks = [Landmark(llayer, l) for l in llayer.get_features(bbox=bbox)]
                floor.add_landmarks(landmarks)

        return buildings

    def get_landmarks(self):
        layer = self.__layers['landmarks']
        query = '"indoor" = \'no\''
        return [Landmark(layer, f) for f in layer.get_features(query=query)]

    def get_paths(self):
        layer = self.__layers['paths']
        return [Path(layer, f) for f in layer.get_features()]

    def get_layers(self):
        return self.__layers

    def add_feature(self, layer, name, geom):
        return self.__layers[layer].add_feature(name, geom)
