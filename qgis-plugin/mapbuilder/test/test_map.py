# coding=utf-8
"""Dialog test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'chebizarro@gmail.com'
__date__ = '2018-10-19'
__copyright__ = 'Copyright 2018, Chris Daley'


import sys
import unittest

from mapbuilder.referencepoint import map

class MapTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_new_map(self):
        mp = map.Map('Test Map')
        mp.createNewMap('Test Map')

if __name__ == "__main__":
    suite = unittest.makeSuite(MapTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)