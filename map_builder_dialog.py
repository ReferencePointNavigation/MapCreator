# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapBuilderDialog
                                 A QGIS plugin
 This plugin builds a Reference Point Navigation map
                             -------------------
        begin                : 2018-10-19
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Chris Daley
        email                : chebizarro@gmail.com
 ***************************************************************************/
"""

import os

from PyQt5 import uic
from PyQt5 import QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'map_builder_dialog_base.ui'))


class MapBuilderDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(MapBuilderDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
