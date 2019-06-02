import zipfile
from referencepoint.proto import Building_pb2
from elvis.core import States, Position, MiniMap
from math import floor

class MapReader:

    def __init__(self, config):
        self.config = config
        self.file = config['map']

    def get_buildings(self):
        zf = zipfile.ZipFile(self.file)
        buildings = [zf.read(n) for n in zf.namelist() if n.endswith('.bldg')]
        zf.close()
        return buildings

    def get_building(self, name):
        building_name = name.replace(' ', '_') + '.bldg'
        zf = zipfile.ZipFile(self.file)
        building = [zf.read(n) for n in zf.namelist() if n == building_name]
        zf.close()
        bldg_proto = Building_pb2.Building()
        if len(building) > 0:
            bldg_proto.ParseFromString(building[0])
        return bldg_proto

    def build_map(self):
        building = self.get_building(self.config['building'])
        minimap = None
        landmarks = None
        start_position = None
        end_position = None

        for floors in building.floors:
            if floors.number == self.config['floor']:
                flr = floors
                minimap = flr.minimap
                landmarks = flr.landmarks

        tiles = [[States.BLOCKED for n in range(minimap.columns)] for i in range(minimap.rows)]

        for tile in minimap.tiles:
            tiles[tile.row][tile.column] = States.EMPTY

        if landmarks is not None:
            for landmark in landmarks:
                xy = (floor(landmark.location.x - minimap.minCoordinates.x), floor(landmark.location.y - minimap.minCoordinates.y))
                if landmark.name == self.config['start-landmark']:
                    tiles[xy[1]][xy[0]] = States.ACTOR
                    start_position = Position(xy[0], xy[1])
                elif landmark.name == self.config['end-landmark']:
                    tiles[xy[1]][xy[0]] = States.END
                    end_position = Position(xy[0], xy[1])
                else:
                    tiles[xy[1]][xy[0]] = States.LANDMARK

        return MiniMap(tiles, minimap.rows, minimap.columns, start_position, end_position)