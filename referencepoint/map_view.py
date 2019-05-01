

class MapView:

    controller = None
    group = None
    layers = None
    current = None

    def __init__(self, plugin, project):
        self.plugin = plugin
        self.project = project

    def set_controller(self, controller):
        self.controller = controller

    def show(self):
        self.plugin.add_action(
            self.plugin.get_resource('logo'),
            text=self.plugin.tr(u'About Reference Point Navigation'),
            callback=self.rpn_action)

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

        self.plugin.add_separator()

        self.plugin.add_action(
            self.plugin.get_resource('building'),
            text=self.plugin.tr(u'Add Building'),
            callback=self.add_building_action,
            enabled_flag=False)

        self.plugin.add_action(
            self.plugin.get_resource('floor'),
            text=self.plugin.tr(u'Add Floor'),
            callback=self.add_floor_action,
            enabled_flag=False)

        self.plugin.add_action(
            self.plugin.get_resource('landmark'),
            text=self.plugin.tr(u'Add Landmark'),
            callback=self.add_landmark_action,
            enabled_flag=False)

        self.plugin.add_action(
            self.plugin.get_resource('path'),
            text=self.plugin.tr(u'Add Path'),
            callback=self.add_path_action,
            enabled_flag=False)

        self.plugin.add_action(
            self.plugin.get_resource('move'),
            text=self.plugin.tr(u'Move Object'),
            callback=self.move_action,
            enabled_flag=False)

    def rpn_action(self):
        self.plugin.show_help()

    def new_map_action(self):
        title = self.plugin.tr(u'Enter a name for the new Map')
        prompt = self.plugin.tr(u'Name:')
        mapname = self.plugin.show_input_dialog(title, prompt)
        if mapname is not '':
            self.project.clear()
            self.layers = dict()
            self.group = self.project.layerTreeRoot().insertGroup(0, mapname)
            self.controller.new_map(mapname)
            for action in self.plugin.actions:
                action.setEnabled(True)

    def add_layers(self, layers):
        if self.group is not None:
            for layer in layers:
                self.layers[layer.name] = layer.add_to_group(self.group)

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

    def add_building_action(self):
        self.set_active_layer('Buildings')

    def add_floor_action(self):
        self.set_active_layer('Rooms')

    def add_landmark_action(self):
        self.set_active_layer('Landmarks')

    def add_path_action(self):
        self.set_active_layer('Paths')

    def set_active_layer(self, layer):
        if self.current is not None:
            self.current.layer().commitChanges()
        self.current = self.layers[layer]
        self.plugin.set_active_layer(self.current.layer())
        self.current.layer().startEditing()
        self.plugin.set_add_feature()

    def move_action(self):
        if self.current is not None:
            self.plugin.select_move_tool()

    def add_layer(self, name, path):
        layer = self.plugin.new_layer(path, self.plugin.tr(name))
        self.group.addLayer(layer)
        return layer
