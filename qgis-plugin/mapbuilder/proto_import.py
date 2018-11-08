# -*- coding: utf-8 -*-
import sys, os
protos_path = os.path.join(os.path.dirname(__file__), 'proto')
if protos_path not in sys.path:
    sys.path.append(protos_path)

from .proto import BuildingMapProto_pb2
from qgis.core import QgsVectorLayer, QgsProject, QgsFeature, QgsGeometry, QgsPointXY, QgsPolygon

def parseProtobuf(filename):
	map = BuildingMapProto_pb2.BuildingMap()
	
	with open(filename, 'rb') as f:
		map.ParseFromString(f.read())
		parseMap(map)
		
def parseMap(map):
	layers = newLayers(map.name)	

	for floor in map.floors:
		parseFloor(floor, layers)

	for key in layers:
		layers[key].updateExtents()
		QgsProject.instance().addMapLayer(layers[key])

def parseFloor(floor, layers):
	for landmark in floor.landmarks:
		parseLandmark(landmark, layers)
	for ns in floor.navigableSpaces:
		parseNavigableSpaces(ns, layers)

def parseNavigableSpaces(ns, layers):
	layer = layers['polygon']
	pt = newFeature(layer)
	pr = layer.dataProvider()
	geom = geomFromCoordinates(ns.outerBoundary)
	pt.setGeometry(geom)
	pr.addFeatures([pt])
	

def parseLandmark(landmark, layers):
	layer = layers['point']
	pt = newFeature(layer)	
	pr = layer.dataProvider()
	pt.setGeometry(geomFromLocation(landmark.location))
	pt['name'] = landmark.name
	pr.addFeatures([pt])


def newLayers(name):
	
	fields = 'field=name:string(25)'
	
	base_fields = [
		'name:string(25)',
		'level:int()',
		'indoor:string(25)',
	]

	point_fields = base_fields + [
		'type:string(12)',
		'wheelchair:string(25)',
		'amenity:string(25)',
		'access:string(25)'
	]
	
	layers = {
		"point" : QgsVectorLayer('Point?crs=epsg:26911&'+fields, name , "memory"),
		"polygon" : QgsVectorLayer('Polygon?crs=epsg:26911&'+fields, name , "memory"),
	}
	return layers


def geomFromCoordinates(coordinates):
	points = [QgsPointXY(c.x, c.y) for c in coordinates]
	return QgsGeometry.fromPolygonXY([points])
	

def geomFromLocation(location):
	return QgsGeometry.fromPointXY(QgsPointXY(location.x, location.y))

def newFeature(layer):
	f = QgsFeature()
	f.setFields(layer.fields())
	return f
