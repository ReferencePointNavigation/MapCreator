# coding=utf-8
"""
MapExporter test.

"""

__author__ = 'chebizarro@gmail.com'
__date__ = '2019-05-07'
__copyright__ = 'Copyright 2019, Chris Daley'


import unittest
from unittest.mock import Mock, MagicMock, call
from referencepoint import MapImporter
from referencepoint.proto import Building_pb2, Map_pb2

class MapImporterTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_new_map_importer(self):
        test_map = Mock()
        reader = Mock()
        exporter = MapImporter(test_map, reader)
        assert exporter is not None

    def test_map_exporter_export(self):

        test_map = Mock()
        test_map.get_name.return_value = 'Test'

        m = MagicMock()

        test_map.add_feature.return_value = m

        map_proto = Map_pb2.Map()
        map_proto.name = 'Test'
        for x, y in [(0,0), (10,0), (10,10), (0,10)]:
            pt = map_proto.buildings['Test Building'].vertices.add()
            pt.x = x
            pt.y = y

        bldg = Building_pb2.Building()
        bldg.name = "Test Building"
        flr = bldg.floors.add()
        flr.number = 0
        rm = flr.navigableSpaces.add()
        for x, y in [(0.1, 0.1), (9.9, 0.1), (9.9, 9.9), (0.1, 9.9)]:
            pt = rm.outerBoundary.add()
            pt.x = x
            pt.y = y

        lm = flr.landmarks.add()
        point = [0.2, 0.2]
        lm.name = 'Test Landmark'
        lm.type = 1
        lm.location.x = point[0]
        lm.location.y = point[1]

        reader = Mock()
        reader.get_map.return_value = map_proto.SerializeToString()
        reader.get_building.return_value = bldg.SerializeToString()

        importer = MapImporter(test_map, reader)
        importer.import_map()

        calls = [
            call('buildings', 'Test Building', map_proto.buildings['Test Building'].vertices),
            call('rooms', '', rm.outerBoundary),
            call('landmarks', 'Test Landmark', lm.location)
        ]

        test_map.add_feature.has_calls(calls)


class MockPoint:
    def __init__(self, point):
        self.point = point

    def x(self):
        return self.point[0]

    def y(self):
        return self.point[1]


if __name__ == "__main__":
    unittest.main()
