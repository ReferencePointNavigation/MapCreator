"""
Imports Map definition from Protobuf files
"""
import zipfile
import os, sys

protos_path = os.path.join(os.path.dirname(__file__), 'proto')
if protos_path not in sys.path:
    sys.path.append(protos_path)

from referencepoint.proto import Map_pb2


class MapImporter:

    def __init__(self, map):
        self.map = map

    def import_map(self, file):

        zf = zipfile.ZipFile(file)
        f, _ = os.path.splitext(file)
        data = zf.read(f)

        map_proto = Map_pb2.Map()
        map_proto.ParseFromString(data)
        self.map.name = map_proto.name
        self.map.description = map_proto.description

        for building in map_proto.buildings:
            self.import_building(building)

        for path in map_proto.paths:
            pass

        for landmark in map_proto.landmarks:
            pass

    def import_building(self, building):
        pass

    def import_path(self, path):
        pass

    def import_landmark(self, landmark):
        pass
