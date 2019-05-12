from .qgs_widget import QgsWidget


class DisplayWidget(QgsWidget):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if 'display' not in QgsWidget.registry.keys():
            QgsWidget.registry['display'] = []
        QgsWidget.registry['display'].append(cls)

    def __init__(self, iface, icon, text):
        super().__init__(iface, icon, text)
        self.setEnabled(False)


class ShowGridWidget(DisplayWidget):

    def __init__(self, iface):
        super().__init__(iface, 'grid', u'Show Grid')

    def action(self):
        pass


class ShowLevelMenu(DisplayWidget):

    def __init__(self, iface):
        super().__init__(iface, 'floors', u'Show Floors')

    def action(self):
        pass