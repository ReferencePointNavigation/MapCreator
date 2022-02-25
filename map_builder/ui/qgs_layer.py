from qgis.core import (
    Qgis,
    QgsVectorLayer,
    QgsFeatureRequest,
    QgsDefaultValue,
    QgsCoordinateReferenceSystem,
    QgsEditorWidgetSetup,
    QgsFeature,
    QgsGeometry,
    QgsMessageLog,
    QgsPointXY,
    QgsRectangle,
    QgsPalLayerSettings,
    QgsVectorLayerSimpleLabeling
)

import qgis.utils
from PyQt5.QtCore import pyqtSignal, QObject


class Layer(QObject):

    def __init__(self, name, geom_type, crs):
        super().__init__()
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
        settings = QgsPalLayerSettings()
        settings.fieldName = 'name'
        labeling = QgsVectorLayerSimpleLabeling(settings)
        self.layer.setLabeling(labeling)
        self.layer.setLabelsEnabled(True)
        self.layer.committedFeaturesAdded.connect(self.on_feature_added)
        self.node = None

    # overriden by subclasses
    def on_feature_added(self):
        pass

    def add_to_group(self, group):
        self.node = group.addLayer(self.layer)
        self.node.setCustomProperty("showFeatureCount", True)
        return self.node

    def start_editing(self):
        self.layer.startEditing()

    def get_features(self, query=None, bbox=None):

        old_substring = self.layer.subsetString()
        self.layer.setSubsetString(None)
        self.layer.updateExtents(True)

        if bbox is not None:
            self.filter.setFilterRect(bbox)
        else:
            self.filter.setFilterRect(QgsRectangle())

        if query is not None and self.query is not None:
            self.filter.setFilterExpression('{0} and {1}'.format(self.query, query))
        elif query is not None:
            self.filter.setFilterExpression(query)
        elif self.query is not None:
            self.filter.setFilterExpression(self.query)
        else:
            self.filter.setFilterExpression('')

        features = self.layer.getFeatures(self.filter)

        self.layer.setSubsetString(old_substring)
        self.layer.updateExtents(True)

        return features

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

    # noinspection PyMethodMayBeStatic
    def new_layers(self, crs='3857'):

        return {
            'landmarks': LandmarkLayer(crs),
            'paths': PathLayer(crs),
            'rooms': RoomLayer(crs),
            'buildings': BuildingLayer(crs)
        }

    # noinspection PyMethodMayBeStatic
    def get_base_map_layer(self):
        return BaseMapLayer()


class BuildingLayer(Layer):
    def __init__(self, crs):
        self.fields = ['building:string(25)']
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

        #self.subscribe(self.on_level_selected, Topics.LEVEL_SELECTED)

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

    def set_level(self, level):
        self.layer.setSubsetString(None)
        if level is not None:
            self.layer.setSubsetString('"level"=\'{}\''.format(level))
        self.layer.updateExtents(True)


class PathLayer(Layer):
    def __init__(self, crs):
        super().__init__(u'Paths', 'Linestring', crs)


class RoomLayer(Layer):

    levels_changed = pyqtSignal()

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
        self.levels_changed.emit()
        return feature

    def on_feature_added(self):
        self.levels_changed.emit()

    def set_level(self, level):
        self.layer.setSubsetString(None)
        if level is not None:
            self.layer.setSubsetString('"level"=\'{}\''.format(level))
        self.layer.updateExtents(True)

    def get_levels(self, building=None):
        features = self.layer.getFeatures() if building is None else self.layer.getFeatures(building)

        levels = set()
        for level in features:
            attr = level.attributes()[1]
            if attr is None:
                continue
            else:
                levels.add(int(attr))

        return sorted(levels)


class BaseMapLayer:
    def __init__(self):
        self.layer_type = None
        self.ol_plugin = None
        try:
            self.ol_plugin = qgis.utils.plugins['openlayers_plugin']
            self.layer_type = self.ol_plugin._olLayerTypeRegistry.getById(4)
        except KeyError:
            QgsMessageLog.logMessage("The OpenLayers plugin is not enabled, the base map will not be loaded", "RPN Map Builder", level=Qgis.Info )

    def show(self):
        if self.ol_plugin is not None:
            self.ol_plugin.addLayer(self.layer_type)
