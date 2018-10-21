import sys

import BuildingMapProto_pb2



if __name__== "__main__":
	f = sys.argv[1:]
		
	map = BuildingMapProto_pb2.BuildingMap()
	
	with open(f[0],'rb') as map_contents:
		map.ParseFromString(map_contents.read())
	
	print(len(map.floors))
