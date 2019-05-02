# -*- coding: utf-8 -*-
import zipfile
import os, sys

protos_path = os.path.join(os.path.dirname(__file__), 'proto')
if protos_path not in sys.path:
    sys.path.append(protos_path)

from referencepoint.proto import Map_pb2, Building_pb2


class MapExporter:
    """
    The MapExporter class serializes the map features to the Protobuf
    representation and bundles them together in a zip file with the
    .rpn extension
    """
    def __init__(self, map):
        """
        Constructor
        :param map: A Reference Point Map
        :type map: Map
        """
        self.map = map

    def export_map(self, filepath):
        """
        Export the map to the given file path
        :param filepath: a directory to store the zipped Map files
        :type  filepath: str
        """
        filename = os.path.join(filepath, self.map.name.replace(' ', '_'))
        zf = zipfile.ZipFile(filename + '.rpn', mode='w')

        map_proto = Map_pb2.Map()
        map_proto.name = self.map.name

        buildings = self.map.layers['buildings'].get_features()

        for building in buildings:
            for points in building.geometry().asPolygon()[0]:
                points = self.map.layers['buildings'].transform(points)
                point = map_proto.buildings[building['name']].vertices.add()
                point.x = points.x()
                point.y = points.y()
            bldg = self.__export_buildings(building)

            zf.writestr(building['name'].replace(' ', '_') + '.bldg', bldg.SerializeToString())

        zf.writestr(self.map.name.replace(' ', '_') + '.map', map_proto.SerializeToString())
        zf.close()

    def __export_buildings(self, building):
        bldg = Building_pb2.Building()
        # add floors
        for room in self.map.layers['rooms'].get_features(bbox=building.geometry().boundingBox()):
            if building.geometry().contains(room.geometry()):
                flr = None
                flr_no = int(room['level'])
                for floor in bldg.floors:
                    if floor.number == flr_no:
                        flr = floor
                    else:
                        flr = bldg.floors.add()
                        flr.number = flr_no
                rm = flr.navigableSpaces.add()
                for points in room.geometry().asPolygon()[0]:
                    point = rm.outerBoundary.add()
                    points = self.map.layers['buildings'].transform(points)
                    point.x = points.x()
                    point.y = points.y()
                for landmark in self.map.layers['landmarks'].get_features(bbox=room.geometry().boundingBox()):
                    if room.geometry().contains(landmark.geometry()) and landmark['level'] == room['level']:
                        geom = self.map.layers['buildings'].transform(landmark.geometry().asPoint())
                        lm = flr.landmarks.add()
                        lm.name = landmark['name']
                        lm.type = int(landmark['type'])
                        lm.location.x = geom[0]
                        lm.location.y = geom[1]
        return bldg

