# -*- coding: utf-8 -*-
import zipfile
import os, sys

protos_path = os.path.join(os.path.dirname(__file__), 'proto')
if protos_path not in sys.path:
    sys.path.append(protos_path)

from referencepoint.proto import Map_pb2, Building_pb2

from qgis.core import QgsWkbTypes


class MapExporter:
    """
    The MapExporter class serializes the map features to the Protobuf
    representation and bundles them together in a zip file with the
    .rpn extension
    """
    def __init__(self, map):
        """
        Constructor
        :param map: A Reference Point Map
        :type map: Map
        :param expr: A function which returns a QgsFeatureRequest based on the
            passed query string
        :type expr: FunctionType
        """
        self.map = map

    def export_map(self, filepath):
        """
        Export the map to the given file path
        :param filepath: a directory to store the zipped Map files
        :type  filepath: str
        """
        filename = os.path.join(filepath, self.map.name.replace(' ', '_'))
        zf = zipfile.ZipFile(filename + '.rpn', mode='w')

        map_proto = Map_pb2.Map()
        map_proto.name = self.map.name

        for building in self.export_buildings():
            building_proto = self.export_building(building)
            zf.writestr(building_proto.name.replace(' ', '_'), building_proto.SerializeToString())

        self.export_paths(map_proto)

        self.export_landmarks(map_proto)

        zf.writestr(self.map.name.replace(' ', '_'), map_proto.SerializeToString())
        zf.close()

    def export_buildings(self):
        """
        Build and return a dictionary of all of the buildings in the map
        :return: a dictionary of all of the buildings
        :rtype: dict
        """
        buildings = {}
        query = '"building" = \'yes\' and "name" <> \'NULL\''
        selection = self.map.layers['buildings'].getFeatures(query)

        for building in selection:
            buildings[building['name']] = {'feature': building}

        self.get_floors(buildings)
        return buildings

    def get_floors(self, buildings):
        query = '"indoor" <> \'NULL\''
        floors = {}



        for name, building in buildings.items():

            floors[name] = {}
            for layer in layers:
                selection = layer.getFeatures(query)
                for feature in selection:
                    if building.geometry().intersects(feature.geometry()) and building is not feature:
                        level = int(feature['level'])
                        if level in floors[name]:
                            floors[name][level].append(feature)
                        else:
                            floors[name][level] = [feature]
        return floors

    def export_building(self, building):
        proto = Building_pb2.Building()

        return proto

    def export_paths(self, map_proto):
        pass

    def export_landmarks(self, map_proto):
        pass



    def get_maps(self, layers):
        buildings = self.get_buildings(layers)
        floors = self.get_floors(buildings, layers)
        return self.build_map(buildings, floors)

    def get_buildings(self, layers):
        query = '"building" = \'yes\' and "name" <> \'NULL\''
        buildings = {}

        for layer in layers:
            selection = layer.getFeatures(query)
            for building in selection:
                buildings[building['name']] = building
        return buildings

    def get_floors(self, buildings, layers):
        query = '"indoor"<> \'NULL\''
        floors = {}
        for name, building in buildings.items():
            if name is None:
                continue
            floors[name] = {}
            for layer in layers:
                selection = layer.getFeatures(query)
                for feature in selection:
                    if building.geometry().intersects(feature.geometry()) and building is not feature:
                        level = int(feature['level'])
                        if level in floors[name]:
                            floors[name][level].append(feature)
                        else:
                            floors[name][level] = [feature]
        return floors

    def build_map(self, buildings, floors):
        maps = []
        for name, building in buildings.items():
            buildingMap = self.new_building_map(building)
            maps.append(buildingMap)
            for key, floor in floors[name].items():
                floorMap = buildingMap.floors.add()
                floorMap.number = key
                for feature in floor:
                    self.add_feature(floorMap, feature)

        return maps

    def new_building_map(self, building):
        buildingExtent = building.geometry().boundingBox()
        buildingMap = Building_pb2.Building()
        buildingMap.name = building['name'] or ""
        buildingMap.minCoordinates.x = buildingExtent.xMinimum()
        buildingMap.minCoordinates.y = buildingExtent.yMinimum()
        buildingMap.maxCoordinates.x = buildingExtent.xMaximum()
        buildingMap.maxCoordinates.y = buildingExtent.yMaximum()
        return buildingMap

    def add_feature(self, floorMap, feature):
        """Adds a feature to the provided floor"""
        geomType = feature.geometry().wkbType()

        if geomType == QgsWkbTypes.MultiPolygon:
            self.add_navigable_space(floorMap, feature)
        elif (
                geomType == QgsWkbTypes.LineGeometry and
                feature['name'] is not None and
                feature['type'] is not None
        ):
            self.add_landmark(floorMap, feature)
        else:
            pass

    def add_navigable_space(self, floor, feature):
        geom = feature.geometry().asMultiPolygon()[0][0]
        navigable_space = floor.navigableSpaces.add()
        for points in geom:
            point = navigable_space.outerBoundary.add()
            point.x = points.x()
            point.y = points.y()

    def add_landmark(self, floor, feature):
        geom = feature.geometry().asPoint()
        landmark = floor.landmarks.add()
        landmark.name = feature['name']
        landmark.location.x = geom[0]
        landmark.location.y = geom[1]
        if feature['type'] == 'DOOR':
            landmark.type = 1
        elif feature['type'] == 'HALLWAY_INTERSECTION':
            landmark.type = 2
        elif feature['type'] == 'STAIRS':
            landmark.type = 3
        elif feature['type'] == 'ELEVATOR':
            landmark.type = 4
