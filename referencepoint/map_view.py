import os
from pubsub import pub
from referencepoint import Topics


class MapView:

    def __init__(self, plugin, project):
        self.controller = None
        self.group = None
        self.layers = None
        self.current = None

        self.plugin = plugin
        self.project = project

    def set_controller(self, controller):
        self.controller = controller

    def show(self):
        self.subscribe(self.new_map, Topics.NEW_MAP)
        self.subscribe(self.import_map, Topics.IMPORT_MAP)
        self.subscribe(self.export_map, Topics.EXPORT_MAP)
        self.subscribe(self.tool_selected, Topics.TOOL_SELECTED)

    def new_map(self, arg1):
        self.project.clear()
        self.plugin.show_basemap()
        self.current = None
        self.layers = dict()
        self.group = self.project.layerTreeRoot().insertGroup(0, arg1)
        self.controller.new_map(arg1)
        self.publish(Topics.MAP_CREATED, arg1)

    def import_map(self, arg1):
        mapname, _ = os.path.splitext(os.path.basename(arg1))
        self.new_map(mapname)
        self.controller.import_map(arg1)

    def export_map(self, arg1):
        if self.current is not None:
            self.current.layer().commitChanges()
        self.controller.save_map(arg1)

    def add_layers(self, layers):
        if self.group is not None:
            for layer in layers:
                self.layers[layer.name] = layer.add_to_group(self.group)
                self.layers[layer.name].setCustomProperty("showFeatureCount", True)

    def tool_selected(self, arg1):
        self.set_active_layer(arg1)

    def grid_action(self):
        self.plugin.show_minimap()

    def move_action(self):
        if self.current is not None:
            self.plugin.select_move_tool()

    def set_active_layer(self, layer):
        if self.current is not None:
            self.current.layer().commitChanges()
        self.current = self.layers[layer]
        self.plugin.set_active_layer(self.current.layer())
        self.current.layer().startEditing()
        self.plugin.set_add_feature()

    def add_layer(self, name, path):
        layer = self.plugin.new_layer(path, self.plugin.tr(name))
        self.group.addLayer(layer)
        return layer

    # noinspection PyMethodMayBeStatic
    def publish(self, topic, arg1):
        pub.sendMessage(topic.value, arg1=arg1)

    # noinspection PyMethodMayBeStatic
    def subscribe(self, listener, topic):
        pub.subscribe(listener, topic.value)
