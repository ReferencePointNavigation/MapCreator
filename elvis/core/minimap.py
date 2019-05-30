from elvis.utils import MapReader
from .position import Position

class MiniMap:

    def __init__(self, config):
        reader = MapReader(config['map'])
        building = reader.get_building(config['building'])
        self.minimap = None
        self.landmarks = None
        for floors in building.floors:
            if floors.number == config['floor']:
                floor = floors
                self.minimap = floor.minimap
                self.landmarks = floor.landmarks

        if self.landmarks is not None:
            for landmark in self.landmarks:
                if landmark.name == config['start-landmark']:
                    self.start_position = Position(landmark.location.x, landmark.location.y)
                elif landmark.name == config['end-landmark']:
                    self.end_position = Position(landmark.location.x, landmark.location.y)


    def get_start_position(self):
        return self.start_position

    def get_end_position(self):
        return self.end_position

    def get_height(self):
        return self.minimap.rows * self.minimap.sideSize

    def get_width(self):
        return self.minimap.columns * self.minimap.sideSize