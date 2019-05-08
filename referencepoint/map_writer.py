import os
import zipfile


class MapWriter:

    def __init__(self, map_name, filepath):
        self.filepath = filepath
        self.filename = os.path.join(filepath, map_name.replace(' ', '_'))
        self.zf = zipfile.ZipFile(self.filename + '.rpn', mode='w')

    def add_map(self, map_data):
        self.zf.writestr(self.filename + '.map', map_data)

    def add_building(self, building_name, building_data):
        self.zf.writestr(building_name.replace(' ', '_') + '.bldg', building_data)

    def close(self):
        self.zf.close()
