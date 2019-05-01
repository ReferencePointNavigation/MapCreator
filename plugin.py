# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Plugin
                                 A QGIS plugin
 This plugin builds a Reference Point Navigation map
                              -------------------
        begin                : 2018-10-19
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Chris Daley
        email                : chebizarro@gmail.com
 ***************************************************************************/
"""
import os, sys
from referencepoint import MapBuilder, MapView
from .layer import LayerFactory
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QDialog, QInputDialog, QLineEdit

from qgis.core import QgsProject, QgsVectorLayer, QgsFeatureRequest
from qgis.utils import showPluginHelp
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
import os.path

class Plugin:
    """QGIS Plugin Implementation."""
    def __init__(self, iface):
        """Constructor.
        :param iface: A QGIS interface instance
        :type iface: QgsInterface
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MapBuilder_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Reference Point Map Builder')
        self.toolbar = self.iface.addToolBar(u'Map Builder')
        self.toolbar.setObjectName(u'MapBuilder')
        self.resource_path = ':/plugins/map_builder/resources/'

        self.view = MapView(self, QgsProject.instance())
        self.controller = MapBuilder(self.view, LayerFactory())

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MapBuilder', message)

    def get_resource(self, name):
        return self.resource_path + name + '.svg'

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """
        if parent is None:
            parent = self.iface.mainWindow()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def add_separator(self):
        self.toolbar.addSeparator()

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.view.show()

    def show_open_dialog(self, title):
        qfd = QFileDialog()
        f = QFileDialog.getOpenFileName(qfd, title, '~')
        return f[0]

    def show_save_folder_dialog(self, title):
        qfd = QFileDialog()
        qfd.setFileMode(QFileDialog.DirectoryOnly)
        if qfd.exec_() == QDialog.Accepted:
            return qfd.selectedFiles()[0]
        else:
            return None

    def show_input_dialog(self, title, prompt):
        text, _ = QInputDialog.getText(self.iface.mainWindow(), title, prompt, QLineEdit.Normal, '')
        return text

    def show_help(self):
        showPluginHelp()

    def select_move_tool(self):
        self.iface.actionMoveFeature().trigger()

    def set_active_layer(self, layer):
        self.iface.setActiveLayer(layer)

    def set_add_feature(self):
        self.iface.actionAddFeature().trigger()

    def unload(self):
        """Disconnect the LayerChanged Signal"""
        #self.iface.currentLayerChanged.disconnect()

        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Reference Point Map Builder'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


