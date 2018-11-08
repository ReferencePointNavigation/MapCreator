# -*- coding: utf-8 -*-
from .proto import BuildingMapProto_pb2
from qgis.core import QgsVectorLayer, QgsProject, QgsFeature, QgsGeometry,
	QgsPointXY, QgsPolygon, QgsWkbTypes, QgsSpatialIndex


class NavatarMap:
	def __init__(self):
		self.index = QgsSpatialIndex()
		
		
	def export_map(self, filepath):
		build_map()
		for building in self.maps:
			with open(filepath + building.name, "wb") as f:
				f.write(building.SerializeToString())
		
	def build_map(self):
		layers = [name, layer for name, layer in QgsProject.instance().mapLayers().items() if type(layer) == QgsVectorLayer]
		buildings = get_buildings(layers)
		floors = get_floors(buildings, layers)

	def get_buildings(self, layers):
		query = '"building" = \'yes\''
		buildings = {}
		
		for layer in layers:
			selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
			for building in selection:
				buildings[building['name']] = building

		return buildings

	def get_floors(self, buildings, layers):
		query = '"indoor"<> \'NULL\''
		floors = {}

		for name, building in buildings:
			floors[name] = {}
			for layer in layers:
				selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
				for feature in selection:
					if building[1].geometry().intersects(feature.geometry()):
						level = int(feature['level'])
						if level in floors[name]:
							floors[name][level].append(feature)
						else:
							floors[name][level] = [feature]

		return floors
	
def addFeature(floor, feature):
	"""Adds a feature to the provided floor"""
	
	geom = feature.geometry()
	points = None
	
	if geom.wkbType() == QgsWkbTypes.MultiPolygon:
		points = geom.asMultiPolygon()[0][0]
	elif geom.wkbType() == QgsWkbTypes.Polygon:
		points = geom.asPolygon()[0]


				
			navigable_space = floor.navigableSpaces.add()
			geom = feature.geometry()
		
		
		if layer.wkbType() in [3, 6]:
			processPolygonLayer(buildingMap, layer)

		elif layer.wkbType() is [1, 4]:
			processPointLayer(layer)
	
	for level, features in floors.items():		
		floor = buildingMap.floors.add()
		floor.number = int(level)
		for feature in features:
			navigable_space = floor.navigableSpaces.add()


			for gpoint in points:
				point = navigable_space.outerBoundary.add()
				point.x = gpoint.x()
				point.y = gpoint.y()


def addPolygon(floor, feature):

	points = geom.asMultiPolygon()[0][0]
	points = geom.asPolygon()[0]

def addPoint(floor, feature):	
	points = geom.asMultiPoint()[0]
	points = geom.asPoint()[0]

	landmark = floor.landmarks.add()
	landmark.name = feature['name']
	landmark.location.x = 

def addLine(floor, feature):
	points = geom.asPolygon()[0]
	
	
def addFeature(floor, feature):
	geomType = feature.geometry().wkbType()

	if geomType in [QgsWkbTypes.MultiPolygon, QgsWkbTypes.Polygon]:
		addPolygon(floor, feature)
	elif geomType in [QgsWkbTypes.MultiPoint, QgsWkbTypes.Point]:
		addPoint(floor, feature)
	elif geomType in [QgsWkbTypes.LineGeometry]:
		addLine(floor, feature)

def addBuilding(building):
	buildingExtent = building.geometry().boundingBox()
	buildingMap = BuildingMapProto_pb2.BuildingMap()
	buildingMap.name = building['name']
	buildingMap.minCoordinates.x = buildingExtent.xMinimum()
	buildingMap.minCoordinates.y = buildingExtent.yMinimum()
	buildingMap.maxCoordinates.x = buildingExtent.xMaximum()
	buildingMap.maxCoordinates.y = buildingExtent.yMaximum()
	return buildingMap


def getMaps(buildings, floors):
	maps = []
	
	for name, building in buildings:
		buildingMap = addBuilding(building)
		maps.append(buildingMap)
		for key, floor in floors[name]:
			floorMap = buildingMap.floors.add()
			floorMap.number = key
			for feature in floor:
				addFeature(floorMap, feature)
					
	return maps
	

def getFloors(buildings, layers):
	query = '"indoor"<> \'NULL\''
	floors = {}

	for name, building in buildings:
		floors[name] = {}
		for layer in layers:
			selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
			for feature in selection:
				if building[1].geometry().intersects(feature.geometry()):
					level = int(feature['level'])
					if level in floors[name]:
						floors[name][level].append(feature)
					else:
						floors[name][level] = [feature]

	return floors
	


def exportMap(filename):

	layers = [name, layer for name, layer in QgsProject.instance().mapLayers().items() if type(layer) == QgsVectorLayer]

	buildings = getBuildings(layers)
	
	floors = getFloors(buildings, layers)
	
	maps = getMaps(buildings, floors)
	
	for building in maps:
		with open(filename + building.name, "wb") as f:
			f.write(building.SerializeToString())

