from PyQt5.QtWidgets import QAction, QActionGroup, QMenu
from .qgs_widget import QgsWidget
from referencepoint import Topics


class DisplayWidget(QgsWidget):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if 'display' not in QgsWidget.registry.keys():
            QgsWidget.registry['display'] = []
        QgsWidget.registry['display'].append(cls)

    def __init__(self, iface, icon, text):
        super().__init__(iface, icon, text)
        self.setCheckable(True)
        self.setEnabled(False)
        self.subscribe(self.map_created, Topics.MAP_CREATED)

    def map_created(self, arg1):
        self.setEnabled(True)


class ShowGridWidget(DisplayWidget):

    def __init__(self, iface):
        super().__init__(iface, 'grid', u'Show Grid')
        self.toggled.connect(self.on_toggled)

    def on_toggled(self, checked):
        self.publish(Topics.SHOW_MINIMAP, checked)


class ShowLevelMenu(DisplayWidget):

    def __init__(self, iface):
        super().__init__(iface, 'floors', u'Show Floors')
        self.setCheckable(False)
        self.level_menu = QMenu()
        self.setMenu(self.level_menu)
        self.subscribe(self.levels_change, Topics.LEVELS_CHANGE)
        self.subscribe(self.new_room, Topics.NEW_ROOM)
        self.levels = set()
        self.group = QActionGroup(self.iface.mainWindow())
        self.add_action(self.translate('Show all'), None)

    def action(self):
        pass

    def levels_change(self, arg1):
        for room in arg1:
            self.new_room(room)

    def new_room(self, arg1):
        if arg1 in self.levels:
            return
        self.levels.add(arg1)
        self.levels = set(sorted(self.levels))
        self.add_action(str(arg1), arg1)

    def add_action(self, name, value):
        action = QAction(name, self.iface.mainWindow())
        action.setCheckable(True)
        action.triggered.connect(lambda b: self.publish(Topics.LEVEL_SELECTED, value))
        self.level_menu.addAction(action)
        self.group.addAction(action)