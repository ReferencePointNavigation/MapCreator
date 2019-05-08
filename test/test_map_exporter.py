# coding=utf-8
"""
MapExporter test.

"""

__author__ = 'chebizarro@gmail.com'
__date__ = '2019-05-04'
__copyright__ = 'Copyright 2019, Chris Daley'


import unittest
from unittest.mock import Mock
from referencepoint import MapExporter


class MapExporterTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_new_map_exporter(self):
        test_map = Mock()
        writer = Mock()
        exporter = MapExporter(test_map, writer)
        assert exporter is not None

    def test_map_exporter_export(self):

        test_map = Mock()
        test_map.get_name.return_value = 'Test'

        b1 = Mock()
        b1.get_name.return_value = 'Test Building'
        b1.get_geometry.return_value = [
            MockPoint((0, 0)),
            MockPoint((10, 0)),
            MockPoint((10, 10)),
            MockPoint((0, 10))
        ]

        test_map.get_buildings.return_value = [b1]
        test_map.get_landmarks.return_value = []

        f1 = Mock()
        f1.get_number.return_value = 0

        b1.get_floors.return_value = [f1]

        r1 = Mock()
        r1.get_geometry.return_value = [
            MockPoint((0.1, 0.1)),
            MockPoint((9.9, 0.1)),
            MockPoint((9.9, 9.9)),
            MockPoint((0.1, 9.9))
        ]

        f1.get_rooms.return_value = [r1]
        f1.contains.side_effect = [False, True]

        bb = Mock()
        bb.xMinimum.return_value = 0.1
        bb.yMinimum.return_value = 0.1
        bb.xMaximum.return_value = 9.9
        bb.yMaximum.return_value = 9.9

        f1.get_bounding_box.return_value = bb

        lm1 = Mock()
        lm1.get_name.return_value = 'Door'
        lm1.get_type.return_value = 1
        lm1.get_geometry.return_value = MockPoint((0.2, 0.2))

        f1.get_landmarks.return_value = [lm1]

        writer = Mock()

        exporter = MapExporter(test_map, writer)
        exporter.export_map()



class MockPoint:
    def __init__(self, point):
        self.point = point

    def x(self):
        return self.point[0]

    def y(self):
        return self.point[1]


if __name__ == "__main__":
    unittest.main()
