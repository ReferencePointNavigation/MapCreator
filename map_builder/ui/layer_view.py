from qgis.core import QgsProject


class LayerView:

    def __init__(self, iface, controller, name=u'Untitled'):
        self.name = name
        self.controller = controller
        self.controller.add_view('layer-view', self)
        self.group = None
        self.iface = iface
        self.layers = {}
        self.current = None

    def import_project(self, group):
        self.name = group.name()
        self.group = group
        for layer in self.group.findLayers():
            self.layers[layer.name()] = layer

    def new_project(self, name, layers, basemap):
        project = QgsProject.instance()
        project.clear()
        basemap.show()
        self.group = project.layerTreeRoot().insertGroup(0, name)
        self.name = name
        self.current = None
        for nm, layer in layers.items():
            self.layers[nm] = layer.add_to_group(self.group)
        self.iface.setActiveLayer(self.layers['buildings'].layer())

    def set_active_layer(self, layer):
        if self.current is not None:
            self.current.layer().commitChanges()
        self.current = self.layers[layer.lower()]
        self.iface.setActiveLayer(self.current.layer())
        self.current.layer().startEditing()
