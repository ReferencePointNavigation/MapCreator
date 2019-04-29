"""
Imports Map definition from Protobuf files
"""
from .protobuf import Building_pb2


class MapImporter():

    def __init__(self, file):
        self.file = file

    def parse(self):
        map = Building_pb2.Building()

        with open(self.file, 'rb') as f:
            map.ParseFromString(f.read())

