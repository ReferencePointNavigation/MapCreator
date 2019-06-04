

class MapView:

    def __init__(self, iface, minimap, controller):
        self.iface = iface
        self.controller = controller
        self.controller.add_view('map-view', self)
        self.minimap = minimap
        self.layers = None
        self.current = None

    def show(self):
        pass

    def add_feature(self):
        self.iface.actionAddFeature().trigger()

    def move_feature(self):
        self.iface.actionMoveFeature().trigger()

    def show_minimap(self, enabled):
        self.minimap.setVisible(enabled)

    def set_level(self, level):
        self.minimap.set_level(level)
