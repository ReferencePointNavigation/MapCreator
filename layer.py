from qgis.core import (
    QgsVectorLayer,
    QgsFeatureRequest,
    QgsDefaultValue,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsEditorWidgetSetup)

class Layer(object):

    def __init__(self, name, geom_type, crs):
        self.crs = crs
        self.query = None
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

    def add_to_group(self, group):
        return group.addLayer(self.layer)

    def start_editing(self):
        self.layer.startEditing()

    def get_features(self):
        if self.query is not None:
            return self.layer.getFeatures(QgsFeatureRequest().setFilterExpression(self.query))
        else:
            return self.layer.getFeatures()

    def transform(self, point, src=None, dest='4326'):
        if src is None:
            src = self.crs
        tf= QgsCoordinateTransform(
            QgsCoordinateReferenceSystem("EPSG:" + src),
            QgsCoordinateReferenceSystem("EPSG:" + dest),
            QgsProject.instance())
        return tf.transform(point)

    def transform_polygon(self, polygon, src=None, dest='4326'):
        if src is None:
            src = self.crs
        tf= QgsCoordinateTransform(
            QgsCoordinateReferenceSystem("EPSG:" + src),
            QgsCoordinateReferenceSystem("EPSG:" + dest),
            QgsProject.instance())
        tf.transformPolygon(polygon)
        return polygon



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


class LandmarkLayer(Layer):
    def __init__(self, crs):
        self.fields = ['indoor:string(25)', 'type:string(12)']
        super().__init__(u'Landmarks', 'Point', crs)
        self.layer.setEditorWidgetSetup(3,
            QgsEditorWidgetSetup("ValueMap",
                {'map': [
                    {'DOOR': '1'},
                    {'HALLWAY_INTERSECTION': '2'},
                    {'STAIRS': '3'},
                    {'ELEVATOR':'4'}]}))


class PathLayer(Layer):
    def __init__(self, crs):
        super().__init__(u'Paths', 'Linestring', crs)


class RoomLayer(Layer):
    def __init__(self, crs):
        self.fields = ['indoor:string(25)']
        super().__init__(u'Rooms', 'Polygon', crs)
        self.query = '"indoor"<> \'NULL\''
        self.layer.setDefaultValueDefinition(2, QgsDefaultValue('\'yes\''))
