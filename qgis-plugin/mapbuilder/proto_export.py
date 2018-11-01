# -*- coding: utf-8 -*-
from .proto import BuildingMapProto_pb2
from qgis.core import QgsVectorLayer, QgsProject, QgsFeature, QgsGeometry,
	QgsPointXY, QgsPolygon, QgsWkbTypes, QgsSpatialIndex

	
def addFeature(floor, feature):
	
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


	
def processLayers(buildings, layers, index):

	query = '"indoor"<> \'NULL\''
	
	for name, layer in layers if layer.type() is QgsMapLayer.VectorLayer:
		selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
		for feature in selection:
	
	floors = {}

	for name, layer in layers if layer.type() is QgsMapLayer.VectorLayer:

		for feature in layer.getFeatures():
			if 'level' in feature.fields().names():
				level = feature['level']
				if level in floors:
					floors[level].append(feature)
				else:
					floors[level] = [feature]		

	for level, features in floors.items():		
		floor = buildingMap.floors.add()
		floor.number = int(level)

		for feature in features:
			addFeature(floor, feature)

def getLandmarks(buildings, layers):
	
	
	

def getBuildings(layers, index):
	query = '"building" = \'yes\''
	buildings = []
	
	for layer in layers:
		selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
		for building in selection:
			index.insertFeature(building)
			building_extent = building.geometry().boundingBox()
			buildingMap = BuildingMapProto_pb2.BuildingMap()
			buildingMap.name = building['name']
			buildingMap.minCoordinates.x = building_extent.xMinimum()
			buildingMap.minCoordinates.y = building_extent.yMinimum()
			buildingMap.maxCoordinates.x = building_extent.xMaximum()
			buildingMap.maxCoordinates.y = building_extent.yMaximum()
			buildings.append(buildingMap)

	return buildings


def exportMap(filename):

	layers = [name, layer for name, layer in QgsProject.instance().mapLayers().items() if type(layer) == QgsVectorLayer]

	index = QgsSpatialIndex()

	buildings = getBuildings(layers, index)
	
	processLayers(buildings, layers, index)

	for building in buildings:
		with open(filename + building.name, "wb") as f:
			f.write(building.SerializeToString())

