# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Plugin
                                 A QGIS plugin
 This plugin builds a Reference Point Navigation map
                              -------------------
        begin                : 2018-10-19
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Chris Daley
        email                : chebizarro@gmail.com
 ***************************************************************************/
"""
import os

from rpn.map_builder import MapBuilder
from rpn.map_view import MapView
from ui import (
  LayerFactory,
  QgsMap,
  MiniMap,
  Toolbar,
  LayerView
)
from PyQt5.QtCore import (
  QSettings,
  QTranslator,
  qVersion,
  QCoreApplication
)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

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

        self.map = QgsMap()
        self.controller = MapBuilder(self.map, LayerFactory())
        self.toolbar = Toolbar(iface, self.tr(u'Map Builder'), self.controller)
        self.grid = MiniMap(self.iface.mapCanvas(), self.map)
        self.view = MapView(iface, self.grid, self.controller)
        self.layer_view = LayerView(self.iface, self.controller)

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
        parent=None,
        checked=False
    ):
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

        :param checked: whether the action should be checkable.
            In the toolbar it will create a Toggle Button

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
        action.setCheckable(checked)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.add_action(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.view.show()

    def show_help(self):
        showPluginHelp()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Reference Point Map Builder'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        self.toolbar.unload()
        del self.toolbar
        del self.view
        del self.controller
        del self.map
        del self.layer_view
