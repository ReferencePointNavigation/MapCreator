from .ui import ElvisWidget


class ElvisToolbar:

    def __init__(self, iface, elvis):
        self.iface = iface
        self.toolbar = self.iface.addToolBar('ELVIS')
        self.toolbar.setObjectName('ELVIS')
        self.actions = []
        self.elvis = elvis

        for cls in ElvisWidget.registry:
            self.add_action(cls(self.iface, self.elvis))

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
