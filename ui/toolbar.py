from ui.qgs_widget import QgsWidget


class Toolbar:

    registry = {}

    def __init__(self, iface, name):
        self.iface = iface
        self.toolbar = self.iface.addToolBar(name)
        self.toolbar.setObjectName(name)
        self.actions = []

        for group, class_list in QgsWidget.registry.items():
            for cls in class_list:
                self.add_action(cls(self.iface))
            self.add_separator()


    def add_action(self, action):
        self.actions.append(action)
        self.toolbar.addAction(action)

    def add_separator(self):
        self.toolbar.addSeparator()
