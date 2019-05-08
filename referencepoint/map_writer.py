import os
import zipfile


class MapWriter:

    def __init__(self, map_name, filepath):
        self.filepath = filepath
        self.filename = map_name.replace(' ', '_')
        self.zf = None

    def add_map(self, map_data):
        self.zf = zipfile.ZipFile(os.path.join(self.filepath, self.filename) + '.rpn', mode='w')
        self.zf.writestr(self.filename + '.map', map_data)

    def add_building(self, building_name, building_data):
        if self.f is not None:
            self.zf.writestr(building_name.replace(' ', '_') + '.bldg', building_data)

    def close(self):
        self.zf.close()
