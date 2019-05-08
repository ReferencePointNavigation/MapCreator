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
        exporter = MapExporter(test_map)
        assert exporter is not None

    def test_map_exporter_export(self):

        test_map = Mock()
        test_map.get_name.return_value = 'Test'

        b1 = Mock()
        b1.get_name.return_value = 'Test Building'
        b1.get_geometry.return_value = [
            MockPoint((155.87851779766901927, -1.85569664044845695)),
            MockPoint((154.641386704023667675, 240.62199771148107175)),
            MockPoint((385.98490121327563429, 238.14773552421650038)),
            MockPoint((387.22203230690774944, -6.80422101497759968)),
            MockPoint((155.87851779766901927, -1.85569664044845695))
        ]

        test_map.get_buildings.return_value = [b1]
        test_map.get_landmarks.return_value = []

        f1 = Mock()
        f1.get_number.return_value = 0

        b1.get_floors.return_value = [f1]

        r1 = Mock()
        r1.get_geometry.return_value = [
            MockPoint((168.24982873399198979, 228.25068677515815807)),
            MockPoint((373.61359027695266377, 225.77642458789355828)),
            MockPoint((377.32498355784946398, 11.75274538950679926)),
            MockPoint((168.24982873399198979, 14.22700757677137062)),
            MockPoint((168.24982873399198979, 228.25068677515815807))
        ]

        f1.get_rooms.return_value = [r1]

        bb = Mock()
        bb.xMinimum.return_value = 168.24982873399198979
        bb.yMinimum.return_value = 11.75274538950679926
        bb.xMaximum.return_value = 377.32498355784946398
        bb.yMaximum.return_value = 228.25068677515815807

        f1.get_bounding_box.return_value = bb

        lm1 = Mock()
        lm1.get_name.return_value = 'Door'
        lm1.get_type.return_value = 1
        lm1.get_geometry.return_value = MockPoint((282.06588934816295478, 17.93840085766828452))

        f1.get_landmarks.return_value = [lm1]

        exporter = MapExporter(test_map)
        files = exporter.export_map()

        assert files[0].name == 'Test'
        assert len(files[0].buildings) == 1
        assert len(files[1][0].floors) == 1
        assert files[1][0].floors[0].number == 0
        assert len(files[1][0].floors[0].navigableSpaces) == 1
        assert files[1][0].floors[0].landmarks[0].name == 'Door'
        assert len(files[1][0].floors[0].landmarks[0].particles) == 10
        #print('No. of tiles: {0}'.format(len(files[1][0].floors[0].minimap.tiles)))


class MockPoint:
    def __init__(self, point):
        self.point = point

    def x(self):
        return self.point[0]

    def y(self):
        return self.point[1]


if __name__ == "__main__":
    unittest.main()
