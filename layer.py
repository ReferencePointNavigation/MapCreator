from qgis.core import (
    QgsVectorLayer,
    QgsFeatureRequest,
    QgsDefaultValue,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsEditorWidgetSetup,
    QgsFeature,
    QgsGeometry,
    QgsPointXY
)

import qgis.utils

class Layer(object):

    def __init__(self, name, geom_type, crs):
        self.crs = crs
        self.query = None
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
        self.layer.setDefaultValueDefinition(0, QgsDefaultValue('\'New {0}\''.format(name[:-1])))
        self.layer.setDefaultValueDefinition(1, QgsDefaultValue('0'))

    def add_to_group(self, group):
        return group.addLayer(self.layer)

    def start_editing(self):
        self.layer.startEditing()

    def get_features(self, query=None, bbox=None):
        if bbox is not None:
            self.filter.setFilterRect(bbox)
        if query is not None:
            self.filter.setFilterExpression(self.query)
        elif self.query is not None:
            self.filter.setFilterExpression(self.query)

        return self.layer.getFeatures(self.filter)

    def transform(self, point, src=None, dest='4326'):
        if src is None:
            src = self.crs
        tf = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem("EPSG:" + src),
            QgsCoordinateReferenceSystem("EPSG:" + dest),
            QgsProject.instance())
        return tf.transform(point)

    def add_feature(self, name, geom):
        return None

    def new_feature(self):
        f = QgsFeature()
        f.setFields(self.layer.fields())
        return f


class LayerFactory:

    def new_layers(self, crs='3857'):

        try:
            olplugin = qgis.utils.plugins['openlayers_plugin']
            ol_gphyslayertype = olplugin._olLayerTypeRegistry.getById(4)
            olplugin.addLayer(ol_gphyslayertype)
        except KeyError:
            pass

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

    def add_feature(self, name, geom):
        feature = self.new_feature()
        points = [self.transform(QgsPointXY(c.x, c.y), src='4326', dest='3857') for c in geom]
        feature.setGeometry(QgsGeometry.fromPolygonXY([points]))
        feature['name'] = name
        self.layer.dataProvider().addFeatures([feature])
        return feature


class LandmarkLayer(Layer):
    def __init__(self, crs):
        self.fields = ['indoor:string(25)', 'type:integer']
        super().__init__(u'Landmarks', 'Point', crs)
        self.layer.setEditorWidgetSetup(3,
            QgsEditorWidgetSetup("ValueMap",
                {'map': [
                    {'DOOR': '1'},
                    {'HALLWAY_INTERSECTION': '2'},
                    {'STAIRS': '3'},
                    {'ELEVATOR':'4'}]}))
        self.layer.setDefaultValueDefinition(3, QgsDefaultValue('1'))

    def add_feature(self, name, geom):
        feature = self.new_feature()
        feature.setGeometry(
            QgsGeometry.fromPointXY(
                self.transform(
                    QgsPointXY(geom.x, geom.y),
                    src='4326',
                    dest='3857')
            )
        )
        feature['name'] = name
        self.layer.dataProvider().addFeatures([feature])
        return feature


class PathLayer(Layer):
    def __init__(self, crs):
        super().__init__(u'Paths', 'Linestring', crs)


class RoomLayer(Layer):
    def __init__(self, crs):
        super().__init__(u'Rooms', 'Polygon', crs)

    def add_feature(self, name, geom):
        feature = self.new_feature()
        points = [self.transform(QgsPointXY(c.x, c.y), src='4326', dest='3857') for c in geom]
        feature.setGeometry(QgsGeometry.fromPolygonXY([points]))
        self.layer.dataProvider().addFeatures([feature])
        return feature

