from qgis.core import (
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsMessageLog,
    Qgis
)

from math import ceil


class Feature(object):

    def __init__(self, feature=None, fields=None):
        self.f = feature
        if feature is None:
            self.f = QgsFeature()
            self.f.setFields(fields)

    def get_name(self):
        return self.f['name']

    def get_bounding_box(self):
        return self.f.geometry().boundingBox()

    def get_geometry(self):
        pass

    def get_feature(self):
        return self.f


class Building(Feature):

    def __init__(self, layer, feature=None):
        super().__init__(layer, feature)
        self.__floors = []

    def add_floors(self, floors):
        self.__floors = floors

    def get_floors(self):
        return self.__floors

    def get_floor(self, level):
        for f in self.__floors:
            if f.get_number() == level:
                return f
        return None

    def get_geometry(self):
        return [p for p in self.f.geometry().asPolygon()[0]]


class Floor:
    def __init__(self, number, layer):
        self.__number = number
        self.__rooms = []
        self.__landmarks = []
        self.__geom = None
        self.__layer = layer
        self.grid = []

    def get_number(self):
        return self.__number

    def add_rooms(self, rooms):
        self.__rooms = rooms
        for room in rooms:
            geom = room.f.geometry()
            if self.__geom is None:
                self.__geom = geom
            else:
                self.__geom = self.__geom.combine(geom)
        self.build_grid()

    def get_rooms(self):
        return self.__rooms

    def add_landmarks(self, landmarks):
        self.__landmarks = landmarks

    def get_landmarks(self):
        return self.__landmarks

    def get_bounding_box(self):
        return self.__geom.boundingBox()

    def get_grid(self):
        return self.grid

    def build_grid(self, tile_size=1.0):
        self.grid = []
        bbox = self.get_bounding_box()
        min_x = bbox.xMinimum()
        min_y = bbox.yMinimum()
        max_x = bbox.xMaximum()
        max_y = bbox.yMaximum()
        rows = max(ceil((max_y - min_y) / tile_size), 0)
        columns = max(ceil((max_x - min_x) / tile_size), 0)
        curr_y = min_y
        curr_x = min_x

        for i in range(0, rows):
            for column in range(0, columns):
                tile = [
                    (curr_x, curr_y),
                    (curr_x + tile_size, curr_y),
                    (curr_x + tile_size, curr_y + tile_size),
                    (curr_x, curr_y + tile_size)
                ]
                if self.intersects(tile):
                    self.grid.append(tile)

                curr_x += tile_size
            curr_x = min_x
            curr_y += tile_size


    def intersects(self, geom):
        points = QgsGeometry.fromPolylineXY(
            [QgsPointXY(p[0], p[1]) for p in geom])
        valid = points.intersects(self.__geom)
        return valid

    def contains(self, geom):
        point = QgsGeometry.fromPointXY(QgsPointXY(geom[0], geom[1]))
        valid = self.__geom.contains(point)
        return valid


class Landmark(Feature):

    def get_type(self):
        return int(self.f['type'])

    def get_geometry(self):
        return self.f.geometry().asPoint()


class Path(Feature):
    pass


class Room(Feature):

    def get_geometry(self):
        return [p for p in self.f.geometry().asPolygon()[0]]


