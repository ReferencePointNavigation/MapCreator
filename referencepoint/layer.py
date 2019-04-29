class Layer(object):
    fields = [
        'name:string(25)',
        'level:integer',
        'indoor:string(25)',
    ]

    def __init__(self, map, name, geom_type, crs):
        self.map = map
        self.name = name
        self.geom_type = geom_type
        self.crs = crs

    def to_string(self):
        return '{0}?crs=epsg:{1}&field={2}'.format(self.geom_type, self.crs, '&field='.join(self.fields))


class LandmarkLayer(Layer):
    def __init__(self, map, name, crs='3857'):
        super().__init__(map, name, 'Point', crs)


class BuildingLayer(Layer):
    def __init__(self, map, name, crs='3857'):
        super().__init__(map, name, 'Polygon', crs)


class PathLayer(Layer):
    def __init__(self, map, name, crs='3857'):
        super().__init__(map, name, 'Linestring', crs)
