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

        try:
            f, _ = os.path.splitext(file)
            data = zf.read(f)
        except KeyError:
            pass
        else:
            map_proto = Map_pb2.Map()
            map_proto.ParseFromString(data)

