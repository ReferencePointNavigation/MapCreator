from .qgs_feature import Building, Floor, Room, Landmark, Path


class QgsMap:

    def __init__(self, name, layer_factory):
        self.name = name
        self.layer_factory = layer_factory
        self.layers = None
        self.crs = 3857

    def new_map(self, name):
        self.name = name
        self.layers = self.layer_factory.new_layers()

    def get_name(self):
        return self.name

    def get_buildings(self, bbox=None):
        layer = self.layers['buildings']
        buildings = [Building(b, layer.fields) for b in layer.get_features(bbox=bbox)]
        for building in buildings:
            floors_layer = self.layers['rooms']
            bbox = building.get_bounding_box()
            floor_nos = sorted(set([int(f['level']) for f in floors_layer.get_features(bbox=bbox)]))
            floors = [Floor(f, floors_layer) for f in floor_nos]
            building.add_floors(floors)
            for floor in floors:
                query = '"level" = \'{}\''.format(floor.get_number())
                rooms = [Room(r, floors_layer.fields) for r in floors_layer.get_features(query=query, bbox=bbox)]
                floor.add_rooms(rooms)
                lm_layer = self.layers['landmarks']
                query += ' and "indoor" = \'yes\''
                landmarks = [Landmark(l, lm_layer.fields) for l in lm_layer.get_features(query=query, bbox=bbox)]
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