from .layer import LandmarkLayer, BuildingLayer, PathLayer

building_query = '"building" = \'yes\' and "name" <> \'NULL\''
floor_query = '"indoor"<> \'NULL\''

point_fields = [
    'type:string(12)',
    'wheelchair:string(25)',
    'amenity:string(25)',
    'access:string(25)'
]


class Map:
    def __init__(self, name='', description=''):
        self.name = name
        self.description = description
        self.layers = dict()
        self.layers['buildings'] = BuildingLayer(self, u'Buildings')
        self.layers['landmarks'] = LandmarkLayer(self, u'Landmarks')
        self.layers['paths'] = PathLayer(self, u'Paths')

    def export(self, filename):
        pass

    @staticmethod
    def import_from_file(filename):
        pass
