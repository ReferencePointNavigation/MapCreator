# -*- coding: utf-8 -*-
import zipfile
import os, sys

protos_path = os.path.join(os.path.dirname(__file__), 'proto')
if protos_path not in sys.path:
    sys.path.append(protos_path)

from referencepoint.proto import Map_pb2, Building_pb2

from qgis.core import QgsWkbTypes


class MapExporter:
    def __init__(self, map, expr):
        self.map = map
        self.filter = expr

    def export_map(self, filepath):

        filename = os.path.join(filepath, self.map.name.replace(' ', '_'))
        zf = zipfile.ZipFile(filename + '.rpn', mode='w')

        map_proto = Map_pb2.Map()
        map_proto.name = self.map.name
        map_proto.description = self.map.description

        for building in self.map.layers['buildings']:
            building_proto = self.export_building(building)
            zf.writestr(building_proto.name.replace(' ', '_'), building_proto.SerializeToString())

        for path in self.map.layers['paths']:
            self.export_path(path, map_proto.paths.add())

        for landmark in self.map.layers['landmarks']:
            self.export_landmark(landmark)

        zf.writestr(self.map.name.replace(' ', '_'), map_proto.SerializeToString())
        zf.close()

    def export_building(self, building):
        proto = Building_pb2.Building()
        query = '"building" = \'yes\' and "name" <> \'NULL\''

        return proto

    def export_path(self, path, proto):
        pass

    def export_landmark(self, landmark):
        pass



    def get_maps(self, layers):
        buildings = self.get_buildings(layers)
        floors = self.get_floors(buildings, layers)
        return self.build_map(buildings, floors)

    def get_buildings(self, layers):
        query = '"building" = \'yes\' and "name" <> \'NULL\''
        buildings = {}

        for layer in layers:
            selection = layer.getFeatures(self.filter(query))
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
                selection = layer.getFeatures(self.filter(query))
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
        buildingMap = BuildingMapProto.Building()
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
