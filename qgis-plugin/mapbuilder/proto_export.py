# -*- coding: utf-8 -*-
from .proto import BuildingMapProto_pb2 as BuildingMapProto
from qgis.core import QgsWkbTypes, QgsFeatureRequest


class RPNMap:
	def __init__(self):
		pass
		
	def export_map(self, layers, filepath):
		maps = self.get_maps(layers)
		for building in maps:
			with open(filepath + "/" + building.name, "wb") as f:
				f.write(building.SerializeToString())
		
	def get_maps(self, layers):	
		buildings = self.get_buildings(layers)
		floors = self.get_floors(buildings, layers)
		return self.build_map(buildings, floors)

	def get_buildings(self, layers):
		query = '"building" = \'yes\' and "name" <> \'NULL\''
		buildings = {}
		
		for layer in layers:
			selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
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
				selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
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
		buildingMap = BuildingMapProto.BuildingMap()
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

