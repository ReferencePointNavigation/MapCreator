# -*- coding: utf-8 -*-

import sys, random

from shapely import Polygon, box
from .BuildingMapProto_pb2 import BuildingMapProto_pb2 as BuildingMapProto


TILE_SIZE = 1.0
NUM_OF_MINIMAP_TILE_LANDMARKS = 5
MAX_LANDMARK_DISTANCE = 20.0
NUM_OF_PARTICLES_PER_LANDMARK = 10



def generateParticles(map):	
	mapBuilder = BuildingMapProto.BuildingMap.MergeFrom(map)
	mapBuilder.clearFloors()
	for floor in map.floors:
		floorBuilder = FloorProto.Floor.MergeFrom(floor)
		floorBuilder.clearLandmarks()
		navigableArea = createAccessibleArea(floor.navigableSpaces)
		for landmark in floor.landmarks:
			radius = 0.5
			while radius < 5.0:
				rect = box(
					landmark.location.x - radius,
					landmark.location.y - radius,
					landmark.location.x + (2 * radius),
					landmark.location.y + (2 * radius))
				intersection = Polygon(navigableArea)
				if rect.intersects(navigableArea):
					break				
				radius += 0.5
			landmarkBuilder = Landmark.MergeFrom(landmark)
			if radius > 5.0:
				pass
			else:
				for i in range(0,NUM_OF_PARTICLES_PER_LANDMARK):
					x,y = 0.0
					while !navigableArea.contains(Point(x, y)):
						x = landmark.location.x + 2 * (random.random() - 0.5) * radius
						x = landmark.location.y + 2 * (random.random() - 0.5) * radius
					coordinatesBuilder = Coordinates(x, y)
					landmarkBuilder.addParticles(coordinatesBuilder)
			floorBuilder.addLandmarks(landmarkBuilder)
		mapBuilder.addFloors(floorBuilder)
	return mapBuilder

	
def generateMinimap(map, tile_size):
	mapBuilder = BuildingMapProto.BuildingMap.MergeFrom(map)
	mapBuilder.clearFloors()
	for floor in map.floors:
		minX = sys.float_info.max
		minY = sys.float_info.max
		maxX = float('-Infinity')
		maxY = float('-Infinity')
		for space in floor.navigableSpaces:
			for vertex in space.outerBoundary:
				if vertex.x > maxX:
					maxX = vertex.x
				if vertex.x < minX:
					minX = vertex.x
				if vertex.y > maxY:
					maxY = vertex.y
				if vertex.y < minY:
					minY = vertex.y
		rows = 
				
		
	
def process(map):
	return generateMinimap(generateParticles(map), TILE_SIZE)
