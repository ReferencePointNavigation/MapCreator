import os
import zipfile
from abc import ABC, abstractmethod
from google.protobuf.json_format import MessageToJson


class MapWriter(ABC):

    def __init__(self, map_name, filepath):
        self.filepath = filepath
        self.filename = map_name.replace(' ', '_')

    @abstractmethod
    def add_map(self, map_data):
      pass

    @abstractmethod
    def add_building(self, building_name, building):
      pass

    @abstractmethod
    def add_path(self, path):
      pass

    @abstractmethod
    def close(self):
      pass


class RPNWriter(MapWriter):

    def __init__(self, map_name, filepath):
      super().__init__(map_name, filepath)
      self.zf = None

    def add_map(self, map_data):
        self.zf = zipfile.ZipFile(os.path.join(self.filepath, self.filename) + '.rpn', mode='w')
        self.zf.writestr(self.filename + '.map', map_data.SerializeToString())

    def add_building(self, building_name, building):
        if self.zf is not None:
            self.zf.writestr(building_name.replace(' ', '_') + '.bldg', building.SerializeToString())

    def add_path(self, path):
      pass

    def close(self):
        self.zf.close()


class JSONWriter(MapWriter):

    def __init__(self, map_name, filepath):
      super().__init__(map_name, filepath)
      self.f = None

    def add_map(self, map_data):
        self.f = open(os.path.join(self.filepath, self.filename) + '.json', 'w')
        self.f.write('"map" : \n{{\n "{}" : {}'.format(self.filename, MessageToJson(map_data)))

    def add_building(self, building_name, building):
        if self.f is not None:
            self.f.write(',\n"{}" : {}'.format(building_name.replace(' ', '_'), MessageToJson(building)))

    def add_path(self, path):
      pass

    def close(self):
      self.f.write('}}')
      self.f.close()
