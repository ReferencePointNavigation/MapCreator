from PyQt5.QtWidgets import QAction, QActionGroup, QToolButton, QMenu
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
        self.setEnabled(False)
        self.subscribe(self.map_created, Topics.MAP_CREATED)

    def map_created(self, arg1):
        self.setEnabled(True)

class ShowGridWidget(DisplayWidget):

    def __init__(self, iface):
        super().__init__(iface, 'grid', u'Show Grid')

    def action(self):
        pass


class ShowLevelMenu(DisplayWidget):

    def __init__(self, iface):
        super().__init__(iface, 'floors', u'Show Floors')
        self.level_menu = QMenu()
        self.setMenu(self.level_menu)


    def action(self):
        pass