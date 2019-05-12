import os
from .qgs_widget import QgsWidget, FileManagerMixin
from qgis.utils import showPluginHelp
from pubsub import pub

class ProjectWidget(QgsWidget, FileManagerMixin):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if 'project' not in QgsWidget.registry.keys():
            QgsWidget.registry['project'] = []
        QgsWidget.registry['project'].append(cls)

    def __init__(self, iface, icon, text):
        super().__init__(iface, icon, text)
        self.setEnabled(True)


class AboutWidget(ProjectWidget):

    def __init__(self, iface):
        super().__init__(iface, 'logo', u'About Reference Point Navigation')

    def action(self):
        showPluginHelp()


class NewMapWidget(ProjectWidget):

    def __init__(self, iface):
        super().__init__(iface, 'new', u'New Reference Point Map')

    def action(self):
        title = self.translate(u'Enter a name for the new Map')
        prompt = self.translate(u'Name:')
        mapname = self.show_input_dialog(self.iface, title, prompt)
        if mapname is not '':
            self.new_map(mapname)

    def new_map(self, mapname):
        pub.sendMessage('new-map', arg1=mapname)


class ImportMapWidget(ProjectWidget):

    def __init__(self, iface):
        super().__init__(iface, 'import', u'Import Reference Point Map')

    def action(self):
        title = self.translate(u'Open File')
        f = self.show_open_dialog(title)
        if len(f) > 2:
            pub.sendMessage('import-map', arg1=f)


class ExportMapWidget(ProjectWidget):

    def __init__(self, iface):
        super().__init__(iface, 'export', u'Export Reference Point Map')

    def action(self):
        title = self.translate(u'Select Directory')
        filepath = self.show_save_folder_dialog(title)
        if filepath is not None:
            pub.sendMessage('export-map', arg1=filepath)

