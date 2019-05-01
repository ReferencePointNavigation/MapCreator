from qgis.core import QgsVectorLayer, QgsFeatureRequest, QgsDefaultValue


class Layer(object):
    fields = [
        'name:string(25)',
        'level:integer',
        'indoor:string(25)',
    ]

    def __init__(self, name, geom_type, crs):
        self.name = name
        path = '{0}?crs=epsg:{1}&field={2}'.format(geom_type, crs, '&field='.join(self.fields))
        self.layer = QgsVectorLayer(path, name, 'memory')
        #self.layer.setDefaultValueDefinition(2, QgsDefaultValue('\'yes\''))

    def add_to_group(self, group):
        return group.addLayer(self.layer)

    def start_editing(self):
        self.layer.startEditing()

    def get_features(self, query):
        return self.layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))


class LayerFactory:

    def new_building_layer(self, crs='3857'):
        return Layer(u'Buildings', 'Polygon', crs)

    def new_landmark_layer(self, crs='3857'):
        return Layer(u'Landmarks', 'Point', crs)

    def new_path_layer(self, crs='3857'):
        return Layer(u'Paths', 'Linestring', crs)

    def new_room_layer(self, crs='3857'):
        return Layer(u'Rooms', 'Polygon', crs)

    def new_layers(self, crs='3857'):
        result = dict()

        result['landmarks'] = self.new_landmark_layer(crs)
        result['paths'] = self.new_path_layer(crs)
        result['rooms'] = self.new_room_layer(crs)
        result['buildings'] = self.new_building_layer(crs)

        return result
