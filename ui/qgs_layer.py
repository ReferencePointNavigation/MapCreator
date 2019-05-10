from qgis.core import (
    QgsVectorLayer,
    QgsFeatureRequest,
    QgsDefaultValue,
    QgsCoordinateReferenceSystem,
    QgsEditorWidgetSetup,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsRectangle
)

class Layer(object):

    def __init__(self, name, geom_type, crs):
        self.crs = crs
        self.query = None
        self.new_count = 0
        self.filter = QgsFeatureRequest()
        fields = [
            'name:string(25)',
            'level:integer'
        ]
        self.name = name
        if hasattr(self, 'fields'):
            self.fields = fields + self.fields
        else:
            self.fields = fields

        path = '{0}?crs=epsg:{1}&field={2}'.format(geom_type, self.crs, '&field='.join(self.fields))
        self.layer = QgsVectorLayer(path, name, 'memory')
        self.layer.setDefaultValueDefinition(1, QgsDefaultValue('0'))

    def add_to_group(self, group):
        return group.addLayer(self.layer)

    def start_editing(self):
        self.layer.startEditing()

    def get_features(self, query=None, bbox=None):
        self.filter.setFilterRect(QgsRectangle())

        if bbox is not None:
            self.filter.setFilterRect(bbox)

        if query is not None and self.query is not None:
            self.filter.setFilterExpression('{0} and {1}'.format(self.query, query))
        elif query is not None:
            self.filter.setFilterExpression(query)
        elif self.query is not None:
            self.filter.setFilterExpression(self.query)

        return self.layer.getFeatures(self.filter)

    def add_feature(self, fields, geom):
        self.layer.setDefaultValueDefinition(0, QgsDefaultValue('\'New {0} {1}\''.format(self.name[:-1], self.new_count)))
        return None

    def new_feature(self):
        f = QgsFeature()
        f.setFields(self.layer.fields())
        return f

    def set_crs(self, crs):
        self.crs = crs
        self.layer.setCrs(QgsCoordinateReferenceSystem(crs))

class LayerFactory:

    def new_layers(self, crs='3857'):

        return {
            'landmarks': LandmarkLayer(crs),
            'paths': PathLayer(crs),
            'rooms': RoomLayer(crs),
            'buildings': BuildingLayer(crs)
        }


class BuildingLayer(Layer):
    def __init__(self, crs):
        self.fields = ['building:string(3)']
        super().__init__(u'Buildings', 'Polygon', crs)
        self.query = '"building" = \'yes\' and "name" <> \'NULL\''
        self.layer.setDefaultValueDefinition(2, QgsDefaultValue('\'yes\''))

    def add_feature(self, fields, geom):
        super().add_feature(fields, geom)
        feature = self.new_feature()
        points = [QgsPointXY(c.x, c.y) for c in geom]
        feature.setGeometry(QgsGeometry.fromPolygonXY([points]))
        for name, value in fields.items():
            feature[name] = value
        feature['building'] = 'yes'
        self.layer.dataProvider().addFeatures([feature])
        return feature


class LandmarkLayer(Layer):
    def __init__(self, crs):
        self.fields = ['indoor:string(25)', 'type:integer']
        super().__init__(u'Landmarks', 'Point', crs)

        self.layer.setEditorWidgetSetup(2,
            QgsEditorWidgetSetup("ValueMap",
                {'map': [
                    {'yes': 'yes'},
                    {'no': 'no'}]}))
        self.layer.setDefaultValueDefinition(2, QgsDefaultValue('\'yes\''))

        self.layer.setEditorWidgetSetup(3,
            QgsEditorWidgetSetup("ValueMap",
                {'map': [
                    {'DOOR': '1'},
                    {'HALLWAY_INTERSECTION': '2'},
                    {'STAIRS': '3'},
                    {'ELEVATOR':'4'}]}))
        self.layer.setDefaultValueDefinition(3, QgsDefaultValue('1'))

    def add_feature(self, fields, geom):
        super().add_feature(fields, geom)
        feature = self.new_feature()
        point = QgsPointXY(geom.x, geom.y)
        feature.setGeometry(
            QgsGeometry.fromPointXY(point)
        )
        for name, value in fields.items():
            feature[name] = value
        self.layer.dataProvider().addFeatures([feature])
        return feature


class PathLayer(Layer):
    def __init__(self, crs):
        super().__init__(u'Paths', 'Linestring', crs)


class RoomLayer(Layer):
    def __init__(self, crs):
        super().__init__(u'Rooms', 'Polygon', crs)

    def add_feature(self, fields, geom):
        super().add_feature(fields, geom)
        feature = self.new_feature()
        points = [QgsPointXY(c.x, c.y) for c in geom]
        for name, value in fields.items():
            feature[name] = value
        feature.setGeometry(QgsGeometry.fromPolygonXY([points]))
        self.layer.dataProvider().addFeatures([feature])
        return feature


