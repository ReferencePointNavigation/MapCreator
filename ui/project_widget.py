from .qgs_widget import QgsWidget
from qgis.utils import showPluginHelp
from .toolbar import Toolbar


class ProjectWidget(QgsWidget):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if 'project' not in Toolbar.registry.keys():
            Toolbar.registry['project'] = []
        Toolbar.registry['project'].append(cls)

    def __init__(self, iface):
        super().__init__(iface)


class AboutWidget(ProjectWidget):

    def __init__(self, iface):
        super().__init__(iface)

    def action(self):
        showPluginHelp()
