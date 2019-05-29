from ui.qgs_widget import QgsWidget


class Toolbar:

    def __init__(self, iface, name):
        self.iface = iface
        self.toolbar = self.iface.addToolBar(name)
        self.toolbar.setObjectName(name)
        self.actions = []

        grp = 0
        for group, class_list in QgsWidget.registry.items():
            grp += 1
            for cls in class_list:
                self.add_action(cls(self.iface))
            if grp < len(QgsWidget.registry):
                self.add_separator()

    def add_action(self, action):
        self.actions.append(action)
        self.toolbar.addAction(action)

    def add_separator(self):
        self.toolbar.addSeparator()

    def unload(self):
        for action in self.actions:
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
