# -*- coding: utf-8 -*-

from .BuildingMapProto_pb2 import BuildingMapProto_pb2 

def parseProtobuf(filename):
	with open(filename, 'r') as f:
		map = BuildingMapProto_pb2.BuildingMap()
		map.ParseFromString(f.read_all())
