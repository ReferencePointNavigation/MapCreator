"""
Imports Map definition from Protobuf files
"""
from .protobuf import Building_pb2, Map_pb2
import zipfile
import os


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

