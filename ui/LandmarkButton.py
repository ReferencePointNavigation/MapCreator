from .UIInterface import UIInterface, UIInterfaceMeta


class LandmarkButton(UIInterface, metaclass=UIInterfaceMeta):

    def __init__(self, plugin):
        super().__init__(plugin)

        self.plugin.add_action(
            self.plugin.resource_path + 'landmark.svg',
            text=self.plugin.tr(u'Add Landmark'),
            callback=None,
            parent=self.plugin.iface.mainWindow())
