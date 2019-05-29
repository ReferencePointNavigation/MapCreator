from .qgs_widget import QgsWidget
from referencepoint import Topics


class ToolWidget(QgsWidget):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if 'tool' not in QgsWidget.registry.keys():
            QgsWidget.registry['tool'] = []
        QgsWidget.registry['tool'].append(cls)

    def __init__(self, iface, icon, text, layer_name):
        super().__init__(iface, icon, text)
        self.setEnabled(False)
        self.layer_name = layer_name
        self.subscribe(self.map_created, Topics.MAP_CREATED)

    def map_created(self, arg1):
        self.setEnabled(True)

    def action(self):
        self.publish(Topics.TOOL_SELECTED, self.layer_name)


class AddBuildingWidget(ToolWidget):

    def __init__(self, iface):
        super().__init__(iface, 'building', u'Add a Building', 'Buildings')


class AddRoomWidget(ToolWidget):

    def __init__(self, iface):
        super().__init__(iface, 'floor', u'Add a Floor', 'Rooms')


class AddLandmarkWidget(ToolWidget):

    def __init__(self, iface):
        super().__init__(iface, 'landmark', u'Add a Landmark', 'Landmarks')


class AddPathWidget(ToolWidget):

    def __init__(self, iface):
        super().__init__(iface, 'path', u'Add a Path', 'Paths')


class MoveWidget(ToolWidget):

    def __init__(self, iface):
        super().__init__(iface, 'move', u'Move an Object', '')

