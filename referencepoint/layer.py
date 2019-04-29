
class Layer(object):
    fields = [
        'name:string(25)',
        'level:integer',
        'indoor:string(25)',
    ]

    def __init__(self, map, name, geom_type, epsg = "3857"):
        self.map = map
        self.name = name
        self.geom_type = geom_type
        self.epsg = epsg
        self.layer = map.add_layer(self)

    def to_string(self):
        return '{0}?crs={0}&field={1}'.format(self.geom_type, self.epsg, '&field='.join(self.fields))


class LandmarkLayer(Layer):
    pass

class BuildingLayer(Layer):
    pass


class PathLayer(Layer):
    pass
