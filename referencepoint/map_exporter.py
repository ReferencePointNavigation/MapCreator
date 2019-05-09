# -*- coding: utf-8 -*-
import os, sys
import random, math

protos_path = os.path.join(os.path.dirname(__file__), 'proto')
if protos_path not in sys.path:
    sys.path.append(protos_path)

from referencepoint.proto import Map_pb2, Building_pb2

TILE_SIZE = 1.0
NUM_OF_MINIMAP_TILE_LANDMARKS = 5
MAX_LANDMARK_DISTANCE = 20.0
NUM_OF_PARTICLES_PER_LANDMARK = 10
NUM_LANDMARK_TYPE = 5


class MapExporter:
    """
    The MapExporter class serializes the map features to the Protobuf
    representation and bundles them together in a zip file with the
    .rpn extension
    """
    def __init__(self, map, writer):
        """
        Constructor
        :param map: A Reference Point Map
        :type map: Map
        :param writer: A MapWriter
        """
        self.map = map
        self.writer = writer

    def export_map(self):
        """
        Export the map to the given file path
        :param filepath: a directory to store the zipped Map files
        :type  filepath: str
        """
        map_proto = Map_pb2.Map()
        map_proto.name = self.map.get_name()

        buildings = {}

        for building in self.map.get_buildings():
            for points in building.get_geometry():
                point = map_proto.buildings[building.get_name()].vertices.add()
                point.x = points.x()
                point.y = points.y()
            bldg = MapExporter.__export_buildings(building)
            buildings[building.get_name()] = bldg.SerializeToString()

        for landmark in self.map.get_landmarks():
            lm = map_proto.landmarks.add()
            point = landmark.get_geometry()
            lm.name = landmark.get_name()
            lm.type = landmark.get_type()
            lm.location.x = point.x()
            lm.location.y = point.y()

        #for path in self.map.get_paths():
            #p = map_proto.paths.add()

        self.writer.add_map(map_proto.SerializeToString())

        for name, building in buildings.items():
            self.writer.add_building(name, building)

        self.writer.close()

    @staticmethod
    def __export_buildings(building):
        bldg = Building_pb2.Building()
        bldg.name = building.get_name()
        for floor in building.get_floors():
            flr = bldg.floors.add()
            flr.number = int(floor.get_number())
            for room in floor.get_rooms():
                rm = flr.navigableSpaces.add()
                for points in room.get_geometry():
                    pts = rm.outerBoundary.add()
                    pts.x = points.x()
                    pts.y = points.y()
            for landmark in floor.get_landmarks():
                lm = flr.landmarks.add()
                point = landmark.get_geometry()
                lm.name = landmark.get_name()
                lm.type = landmark.get_type()
                lm.location.x = point.x()
                lm.location.y = point.y()
                MapExporter.__generate_particles(floor, landmark, lm)
            MapExporter.__generate_minimap(floor, flr, TILE_SIZE)
        return bldg

    @staticmethod
    def __generate_particles(floor, landmark, lm_proto):
        radius = 0.5
        geom = landmark.get_geometry()
        while radius < 5.0:
            rect = [
                (geom.x() - radius, geom.y() - radius),
                (geom.x() + (2 * radius), geom.y() - radius),
                (geom.x() + (2 * radius), geom.y() + (2 * radius)),
                (geom.x() - radius, geom.y() + (2 * radius))
            ]
            if floor.intersects(rect):
                break
            radius += 0.5

        if radius > 5.0:
            pass
        else:
            for i in range(0, NUM_OF_PARTICLES_PER_LANDMARK):
                x, y = 0.0, 0.0
                while not floor.contains([x, y]):
                    x = geom.x() + 2 * (random.random() - 0.5) * radius
                    y = geom.y() + 2 * (random.random() - 0.5) * radius
                particles = lm_proto.particles.add()
                particles.x = x
                particles.y = y

    @staticmethod
    def __generate_minimap(floor, floor_proto, tile_size):

        bbox = floor.get_bounding_box()
        minX = bbox.xMinimum()
        minY = bbox.yMinimum()
        maxX = bbox.xMaximum()
        maxY = bbox.yMaximum()

        rows = max(math.ceil((maxY - minY) / tile_size), 0)
        columns = max(math.ceil((maxX - minX) / tile_size), 0)

        floor_proto.minimap.columns = columns
        floor_proto.minimap.rows = rows
        floor_proto.minimap.sideSize = tile_size
        floor_proto.minimap.minCoordinates.x = minX
        floor_proto.minimap.minCoordinates.y = minY

        curr_y = minY
        curr_x = minX
        for i in range(0, rows):
            for column in range(0, columns):
                tile = [
                    (curr_x, curr_y),
                    (curr_x+tile_size, curr_y),
                    (curr_x+tile_size, curr_y+tile_size),
                    (curr_x, curr_y+tile_size)
                ]
                if floor.intersects(tile):
                    tileBuilder = floor_proto.minimap.tiles.add()
                    tileBuilder.row = i
                    tileBuilder.column = column
                    for ty in range(1, NUM_LANDMARK_TYPE):
                        for lm in MapExporter.__find_closest_landmark(
                                floor,
                                floor_proto,
                                ty, tile):
                            tileBuilder.landmarks.append(lm)
                curr_x += tile_size
            curr_y += tile_size

    @staticmethod
    def __find_closest_landmark(floor, floor_proto, _type, tile):
        ordered_landmarks = []
        index = 0
        for landmark in floor_proto.landmarks:
            if landmark.type is _type:
                distance = MapExporter.__distance(
                    (tile[0][0] + tile[2][0])/2,
                    (tile[0][1] + tile[2][1])/2,
                    landmark.location.x,
                    landmark.location.y
                )

                if MapExporter.__is_accessible([
                            ((tile[0][0] + tile[2][1]) / 2, (tile[0][0] + tile[2][1])/2),
                            (landmark.particles[0].x, landmark.particles[0].y)
                        ], floor):
                    ordered_landmark = (distance, index)
                    ordered_landmarks.append(ordered_landmark)

            index += 1

        ordered_landmarks = sorted(ordered_landmarks, key=MapExporter.__compare_landmarks)
        size = min(len(ordered_landmarks), NUM_OF_MINIMAP_TILE_LANDMARKS)
        return [d[1] for d in ordered_landmarks[:size]]

    @staticmethod
    def __is_accessible(line, floor):
        """
        :return False if line goes outside navigableArea
        """
        for coord in line:
            # Does line have points outside navigableArea?
            if not floor.contains(coord):
                return False
            # Does line intersect the boundaries of navigableArea?
            if floor.intersects(coord):
                return False
        # If none of the above, return True
        return True

    @staticmethod
    def __distance(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        return math.sqrt(dx * dx + dy * dy)

    @staticmethod
    def __compare_landmarks(landmark):
        return landmark[0]
