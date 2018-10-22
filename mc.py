import sys

from google.protobuf.json_format import MessageToJson, Parse

import BuildingMapProto_pb2


def pbToJson(filename, map):
	
	with open(filename,'rb') as map_contents:
		map.ParseFromString(map_contents.read())

	with open('{}.json'.format(filename), 'w') as output:
		output.write(MessageToJson(map))
	
	
def jsonToPB(filename, map):
	
	with open(filename,'r') as json:
		Parse(json.read(), map)
	
	with open('{}.pb'.format(filename), 'wb') as output:
		output.write(map.SerializeToString())


if __name__== "__main__":
	filename = sys.argv[1:][0]
		
	map = BuildingMapProto_pb2.BuildingMap()
	
	
	if filename.endswith('.json'):
		jsonToPB(filename, map)
	else:
		pbToJson(filename, map)
