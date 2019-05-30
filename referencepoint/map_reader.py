import zipfile


class MapReader:

    def __init__(self, map, file):
        self.map = map
        self.file = file
        self.filename = self.map.get_name().replace(' ', '_')
        self.zf = zipfile.ZipFile(self.file)

    def get_map(self):
        map_data = self.zf.read(self.filename + '.map')
        return map_data

    def get_building(self, name):
        bldg_data = self.zf.read(name.replace(' ', '_') + '.bldg')
        return bldg_data

    def close(self):
        if self.zf is not None:
            self.zf.close()
