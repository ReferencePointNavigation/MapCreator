from PyQt5.QtWidgets import QAction, QActionGroup, QMenu
from ui.qgs_widget import QgsWidget


class DisplayWidget(QgsWidget):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if 'display' not in QgsWidget.registry.keys():
            QgsWidget.registry['display'] = []
        QgsWidget.registry['display'].append(cls)

    def __init__(self, iface, controller, icon, text):
        super().__init__(iface, controller, icon, text)
        self.setCheckable(True)
        self.setEnabled(False)
        self.controller.map_created.connect(self.map_created)

    def map_created(self):
        self.setEnabled(True)


class ShowGridWidget(DisplayWidget):

    def __init__(self, iface, controller):
        super().__init__(iface, controller, 'grid', u'Show Grid')
        self.toggled.connect(self.on_toggled)

    def on_toggled(self, checked):
        self.controller.show_minimap(checked)


class ShowLevelMenu(DisplayWidget):

    def __init__(self, iface, controller):
        super().__init__(iface, controller, 'floors', u'Show Floors')
        self.setCheckable(False)
        self.level_menu = QMenu()
        self.setMenu(self.level_menu)
        self.controller.levels_changed.connect(self.levels_change)
        self.levels = set()
        self.group = QActionGroup(self.iface.mainWindow())
        self.add_action(self.translate('Show all'), None)

    def action(self):
        pass

    def levels_change(self):
        for room in self.controller.get_levels():
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
        action.triggered.connect(lambda b: self.controller.set_level(value))
        self.level_menu.addAction(action)
        self.group.addAction(action)