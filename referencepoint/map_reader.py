import os
import zipfile


class MapReader:

    def __init__(self, map, filepath):
        self.map = map
        self.filepath = filepath
        self.filename = os.path.join(filepath, self.map.get_name().replace(' ', '_'))
        self.zf = zipfile.ZipFile(self.filename)
        self.filename, _ = os.path.splitext(os.path.basename(self.filename))

    def get_map(self):
        map_data = self.zf.read(self.filename + '.map')
        return map_data

    def get_building(self, name):
        bldg_data = self.zf.read(name.replace(' ', '_') + '.bldg')
        return bldg_data

    def close(self):
        if self.zf is not None:
            self.zf.close()
