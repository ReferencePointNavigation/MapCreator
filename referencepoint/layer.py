
class Layer(object):
    fields = [
        'name:string(25)',
        'level:integer',
        'indoor:string(25)',
    ]

    def __init__(self, map, name, geom_type, epsg):
        self.map = map
        self.name = name
        self.geom_type = geom_type
        self.epsg = epsg
        self.layer = map.add_layer(self)

    def to_string(self):
        return '{0}?crs={0}&field={1}'.format(self.geom_type, self.epsg, '&field='.join(self.fields))


class LandmarkLayer(Layer):
    def __init__(self, map, name, epsg='3857'):
        super().__init__(map, name, 'Point', epsg)


class BuildingLayer(Layer):
    def __init__(self, map, name, epsg='3857'):
        super().__init__(map, name, 'Polygon', epsg)


class PathLayer(Layer):
    def __init__(self, map, name, epsg='3857'):
        super().__init__(map, name, 'Multiline', epsg)
