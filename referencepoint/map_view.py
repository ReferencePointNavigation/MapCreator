

class MapView:

    controller = None
    group = None

    def __init__(self, plugin, project):
        self.plugin = plugin
        self.project = project

    def set_controller(self, controller):
        self.controller = controller

    def show(self):
        self.plugin.add_action(
            self.plugin.get_resource('new'),
            text=self.plugin.tr(u'New Reference Point Map'),
            callback=self.new_map_action)

        self.plugin.add_action(
            self.plugin.get_resource('import'),
            text=self.plugin.tr(u'Import Reference Point Map'),
            callback=self.open_action)

        self.plugin.add_action(
            self.plugin.get_resource('export'),
            text=self.plugin.tr(u'Export Reference Point Map'),
            callback=self.save_action)

    def new_map_action(self):
        title = self.plugin.tr(u'Enter a name for the new Map')
        prompt = self.plugin.tr(u'Name:')
        mapname = self.plugin.show_input_dialog(title, prompt)
        if mapname is not '':
            self.project.clear()
            self.controller.new_map(mapname)

    def open_action(self):
        title = self.plugin.tr(u'Open File')
        f = self.plugin.show_open_dialog(title)
        if len(f) > 2:
            self.controller.import_map(f)

    def save_action(self):
        title = self.plugin.tr(u'Select Directory')
        dir = self.plugin.show_save_folder_dialog(title)
        if dir is not '':
            self.controller.save_map(dir)

    def add_layer_group(self, name):
        root = self.project.layerTreeRoot()
        self.group = root.insertGroup(0, name)

    def add_layer(self, name, path):
        layer = self.plugin.new_layer(path, self.plugin.tr(name))
        self.group.addLayer(layer)
        return layer
