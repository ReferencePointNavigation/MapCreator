class Toolbar:

    registry = {}

    def __init__(self, iface, name):
        self.iface = iface
        self.toolbar = self.iface.addToolBar(name)
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)
        self.toolbar.addAction(action)

    def add_separator(self):
        self.toolbar.addSeparator()
