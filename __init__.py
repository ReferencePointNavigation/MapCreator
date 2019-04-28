# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapBuilder
                                 A QGIS plugin
 This plugin builds a Reference Point Navigation map
                             -------------------
        begin                : 2018-10-19
        copyright            : (C) 2018 by Chris Daley
        email                : chebizarro@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MapBuilder class from file MapBuilder.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .plugin import MapBuilder
    return MapBuilder(iface)
