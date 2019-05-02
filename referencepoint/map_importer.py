"""
Imports Map definition from Protobuf files
"""
import zipfile
import os, sys

protos_path = os.path.join(os.path.dirname(__file__), 'proto')
if protos_path not in sys.path:
    sys.path.append(protos_path)

from referencepoint.proto import Map_pb2, Building_pb2


class MapImporter:
    """
    The MapImporter class deserializes the the Protobuf representation
    from a zip file with the .rpn extension
    """
    def __init__(self, map):
        """
        Constructor
        :param map: A Reference Point Map
        :type map: Map
        """
        self.map = map

    def import_map(self, file):
        zf = zipfile.ZipFile(file)
        f, _ = os.path.splitext(os.path.basename(file))
        data = zf.read(f + '.map')

        map_proto = Map_pb2.Map()
        map_proto.ParseFromString(data)
        self.map.name = map_proto.name

        for bldg, poly in map_proto.buildings.items():
            bldg_data = zf.read(bldg.replace(' ', '_') + '.bldg')
            bldg_proto = Building_pb2.Building()
            bldg_proto.ParseFromString(bldg_data)
            self.import_building(bldg_proto)

    def import_building(self, building):
        for floor in building.floors:
            for landmark in floor.landmarks:
                self.map.layers['landmarks'].add_feature(landmark.name, landmark.location)

            for room in floor.navigableSpaces:
                self.map.layers['rooms'].add_feature("", room.outerBoundary)
