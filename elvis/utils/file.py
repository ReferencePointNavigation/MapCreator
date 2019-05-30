import zipfile
from referencepoint.proto import Building_pb2


class MapReader:

    def __init__(self, file):
        self.file = file

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
