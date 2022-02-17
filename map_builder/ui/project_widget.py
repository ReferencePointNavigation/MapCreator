from ui.qgs_widget import QgsWidget, FileManagerMixin
from qgis.utils import showPluginHelp


class ProjectWidget(QgsWidget, FileManagerMixin):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if 'project' not in QgsWidget.registry.keys():
            QgsWidget.registry['project'] = []
        QgsWidget.registry['project'].append(cls)

    def __init__(self, iface, controller, icon, text):
        super().__init__(iface, controller, icon, text)
        self.setEnabled(True)


class AboutWidget(ProjectWidget):

    def __init__(self, iface, controller):
        super().__init__(iface, controller, 'logo', u'About Reference Point Navigation')

    def action(self):
        showPluginHelp()


class NewMapWidget(ProjectWidget):

    def __init__(self, iface, controller):
        super().__init__(iface, controller, 'new', u'New Reference Point Map')

    def action(self):
        title = self.translate(u'Enter a name for the new Map')
        prompt = self.translate(u'Name:')
        mapname = self.show_input_dialog(self.iface, title, prompt)
        if mapname != '':
            self.controller.new_map(mapname)


class ImportMapWidget(ProjectWidget):

    def __init__(self, iface, controller):
        super().__init__(iface, controller, 'import', u'Import Reference Point Map')

    def action(self):
        title = self.translate(u'Open File')
        f = self.show_open_dialog(title)
        if len(f) > 2:
            self.controller.import_map(f)


class ExportMapWidget(ProjectWidget):

    def __init__(self, iface, controller):
        super().__init__(iface, controller, 'export', u'Export Reference Point Map')

    def action(self):
        title = self.translate(u'Select Directory')
        filepath = self.show_save_folder_dialog(title)
        if filepath is not None:
            self.controller.save_map(filepath)

