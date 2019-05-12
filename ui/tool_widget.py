from .qgs_widget import QgsWidget
from pubsub import pub


class ToolWidget(QgsWidget):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if 'tool' not in QgsWidget.registry.keys():
            QgsWidget.registry['tool'] = []
        QgsWidget.registry['tool'].append(cls)

    def __init__(self, iface, icon, text, layer_name):
        super().__init__(iface, icon, text)
        self.setEnabled(True)
        self.layer_name = layer_name

    def action(self):
        pub.sendMessage('tool-selected', arg1=self.layer_name)


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

    def action(self):
        pass

