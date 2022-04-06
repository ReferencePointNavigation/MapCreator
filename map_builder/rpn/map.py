
building_query = '"building" = \'yes\' and "name" <> \'NULL\''
floor_query = '"indoor"<> \'NULL\''

point_fields = [
    'type:string(12)',
    'wheelchair:string(25)',
    'amenity:string(25)',
    'access:string(25)'
]


class Map:
    layers = None

    def __init__(self, name):
        self.name = name

    def add_layers(self, layers):
        self.layers = layers

    def export(self, filename):
        pass

    @staticmethod
    def import_from_file(filename):
        pass
