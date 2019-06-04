from .qgs_widget import QgsWidget
from referencepoint import Topics


class ToolWidget(QgsWidget):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if 'tool' not in QgsWidget.registry.keys():
            QgsWidget.registry['tool'] = []
        QgsWidget.registry['tool'].append(cls)

    def __init__(self, iface, controller, icon, text, layer_name):
        super().__init__(iface, controller, icon, text)
        self.setEnabled(False)
        self.layer_name = layer_name
        self.controller.map_created.connect(self.map_created)

    def map_created(self):
        self.setEnabled(True)

    def action(self):
        self.controller.tool_selected(self.layer_name)


class AddBuildingWidget(ToolWidget):

    def __init__(self, iface, controller):
        super().__init__(iface, controller, 'building', u'Add a Building', 'Buildings')


class AddRoomWidget(ToolWidget):

    def __init__(self, iface, controller):
        super().__init__(iface, controller, 'floor', u'Add a Floor', 'Rooms')


class AddLandmarkWidget(ToolWidget):

    def __init__(self, iface, controller):
        super().__init__(iface, controller, 'landmark', u'Add a Landmark', 'Landmarks')


class AddPathWidget(ToolWidget):

    def __init__(self, iface, controller):
        super().__init__(iface, controller, 'path', u'Add a Path', 'Paths')


class MoveWidget(ToolWidget):

    def __init__(self, iface, controller):
        super().__init__(iface, controller, 'move', u'Move an Object', '')

