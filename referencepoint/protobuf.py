# -*- coding: utf-8 -*-

import sys, random, math
import heapq

from shapely import Polygon, box
from .BuildingMapProto_pb2 import BuildingMapProto_pb2 as BuildingMapProto


TILE_SIZE = 1.0
NUM_OF_MINIMAP_TILE_LANDMARKS = 5
MAX_LANDMARK_DISTANCE = 20.0
NUM_OF_PARTICLES_PER_LANDMARK = 10

def isAccessible(line, navigableArea):
	if !navigableArea.contains(line.P1) or !navigableArea.contains(line.P2):
		return False
	start = None
	point1 = None
	point2 = None
	
	for pi in navigableArea:
		coordinates = []
		if ...
		
	return True
		

def findClosestLandmark(k, landmarks, navigableArea, ty, tile):
	comparator = LandmarkComparator()
	orderedLandmarks = []
	heapq.heapify(orderedLandmarks)
	index = 0
	tileArea = tile
	tileArea.intersect(navigableArea)
	for landmark in landmarks:
		if landmark.type = ty:
			distance = tile.centroid.distance(landmark.centroid)
			for pi in...
				coordinates = []
				if pi.currentSegment() != ...
					orderedLandmark = [distance, index]
					orderedLandmarks.append(orederedLandmark)
					break
		index += 1
	size = min(len(orderedLandmarks),k)
	kClosestLandmarks = []
	for i in range(0, size):
		kClosestLandmarks.append(heapq.heappop(orderedLandmarks)[1])
	return kClosestLandmarks

def generateParticles(buildingMap):	
	mapBuilder = BuildingMapProto.BuildingMap.MergeFrom(buildingMap)
	mapBuilder.clearFloors()
	for floor in buildingMap.floors:
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

	
def generateMinimap(buildingMap, tileSize):
	mapBuilder = BuildingMapProto.BuildingMap.MergeFrom(buildingMap)
	mapBuilder.clearFloors()
	for floor in buildingMap.floors:
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
		rows = max(math.ceil((maxX - minY) / tileSize), 0)
		columns = max(math.ceil(maxX - minX) / tileSize), 0)
		landmarks = floor.landmarks
		minimapBuilder = Minimap()
		minimapBuilder.columns = columns
		minimapBuilder.rows = rows
		minimapBuilder.sideSize = tileSize
		minimapBuilder.minCoordinates = Coordinates(minX, minY)
		navigableArea = createAccessibleArea(floor.navigableSpaces)
		currY = minY
		for i in range(0,rows):
			currX = minX
			for column in range(0,columns)
				tile = box(currX, currY, )
				if navigableArea.intersects(tile):
					tileBuilder = Tile()
					tileBuilder.row = row
					tileBuilder.column = column
					for ty in LandmarkType:
						tileBuilder.addAllLandmarks(
							findClosestLandmark(
								NUM_OF_MINIMAP_TILE_LANDMARKS,
								landmarks,
								navigableArea,
								ty, tile)
							)
					minimapBuilder.addTiles(tileBuilder)
				currX += tileSize
			currY += tileSize
		nfloor = Floor()
		nlfoor.miniMap = minimapBuilder
		mapBuilder.addFloors(nfloor)
	
def createAccessibleArea(navigableSpaces):
	for space in navigableSpaces:
		rings = space.rings
		outerBoundary = space.outerBoundary
		first = True
		for vertex in outerBoundary:
			if first:
				navigableSpace.moveTo				
				first = False
			else:
				navigableSpace.lineTo
		if(navigableSpace.currentPoint):
			navigableSpace.closepath
		for ring in rings:
			first = True
			for vertex in ring.polygon:
				if first:
					navigableSpace.moveTo
				else
					navigableSpace.lineTo
				navigableSpace.closePath
		
		return navigableSpace


		
	

def process(buildingMap):
	
	particleMap = generateParticles(buildingMap)
	
	return generateMinimap(particleMap, TILE_SIZE)
