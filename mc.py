import sys, os
import argparse

from google.protobuf.json_format import MessageToJson, Parse

protos_path = os.path.join(os.path.dirname(__file__), 'proto')
if protos_path not in sys.path:
    sys.path.append(protos_path)

from proto import BuildingMapProto_pb2


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

	parser = argparse.ArgumentParser(description
		='Convert InvisiSign Maps between JSON and Protocol Buffer binary format')
	
	parser.add_argument('filename', metavar='FILE', type=str, nargs='+',
						help='a File to process')


	args = parser.parse_args()	
	
	
	filename = sys.argv[1:][0]
		
	map = BuildingMapProto_pb2.BuildingMap()
	
	
	if filename.endswith('.json'):
		jsonToPB(filename, map)
	else:
		pbToJson(filename, map)
