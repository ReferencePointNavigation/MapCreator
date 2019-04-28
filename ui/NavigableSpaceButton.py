from .UIInterface import UIInterface


class NavigableSpaceButton(UIInterface):

    def __init__(self, plugin):
        super().__init__(plugin)

        self.plugin.add_action(
            self.plugin.resource_path + 'floor.svg',
            text=self.plugin.tr(u'Add Navigable Space'),
            callback=None,
            parent=self.plugin.iface.mainWindow())
