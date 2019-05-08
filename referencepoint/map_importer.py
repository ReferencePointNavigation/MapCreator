"""
Imports Map definition from Protobuf files
"""
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
    def __init__(self, map, reader):
        """
        Constructor
        :param map: A Reference Point Map
        :type map: Map
        """
        self.map = map
        self.reader = reader

    def import_map(self):

        map_proto = Map_pb2.Map()
        map_proto.ParseFromString(self.reader.get_map())
        self.map.name = map_proto.name

        for bldg, poly in map_proto.buildings.items():
            self.map.add_feature('buildings', {'name': bldg}, poly.vertices)
            bldg_proto = Building_pb2.Building()
            bldg_proto.ParseFromString(self.reader.get_building(bldg))
            self.import_building(bldg_proto)

        for landmark in map_proto.landmarks:
            self.map.add_feature('landmarks', {
                'name': landmark.name,
                'indoor': 'no',
                'type': str(landmark.type)
            }, landmark.location)

    def import_building(self, building):
        for floor in building.floors:
            for landmark in floor.landmarks:
                self.map.add_feature('landmarks', {
                    'name': landmark.name,
                    'indoor': 'yes',
                    'level': str(floor.number),
                    'type': str(landmark.type)
                }, landmark.location)

            for room in floor.navigableSpaces:
                self.map.add_feature('rooms', {'level': str(floor.number)}, room.outerBoundary)
