from .qgs_feature import Building, Floor, Room, Landmark, Path


class QgsMap:

    def __init__(self, name, layer_factory):
        self.__name = name
        self.__layer_factory = layer_factory
        self.__layers = None
        self.__crs = 3857

    def new_map(self, name):
        self.__name = name
        self.__layers = self.__layer_factory.new_layers()

    def get_name(self):
        return self.__name

    def get_buildings(self, bbox=None):
        layer = self.__layers['buildings']
        buildings = [Building(b, layer.fields) for b in layer.get_features(bbox=bbox)]
        for building in buildings:
            floors_layer = self.__layers['rooms']
            bbox = building.get_bounding_box()
            floor_nos = sorted(set([int(f['level']) for f in floors_layer.get_features(bbox=bbox)]))
            floors = [Floor(f, floors_layer) for f in floor_nos]
            building.add_floors(floors)
            for floor in floors:
                query = '"level" = \'{}\''.format(floor.get_number())
                rooms = [Room(r, floors_layer.fields) for r in floors_layer.get_features(query=query, bbox=bbox)]
                floor.add_rooms(rooms)
                lm_layer = self.__layers['landmarks']
                query += ' and "indoor" = \'yes\''
                landmarks = [Landmark(l, lm_layer.fields) for l in lm_layer.get_features(query=query, bbox=bbox)]
                floor.add_landmarks(landmarks)

        return buildings

    def get_landmarks(self):
        layer = self.__layers['landmarks']
        query = '"indoor" = \'no\''
        return [Landmark(f, layer.fields) for f in layer.get_features(query=query)]

    def get_paths(self):
        layer = self.__layers['paths']
        return [Path(layer, f) for f in layer.get_features()]

    def get_layers(self):
        return self.__layers

    def add_feature(self, layer, fields, geom):
        return self.__layers[layer].add_feature(fields, geom)

    def set_crs(self, crs):
        self.__crs = crs
        for name, layer in self.__layers.items():
            layer.set_crs(crs)

    def get_crs(self):
        return self.__crs