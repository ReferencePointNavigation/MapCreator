from ui.qgs_feature import Building, Floor, Room, Landmark, Path
from PyQt5.QtCore import pyqtSignal, QObject
from rpn import constants

class QgsMap(QObject):
    """Encapsulates the current QGIS Map"""

    map_created = pyqtSignal()
    """Emits an event when a new map is created"""

    levels_changed = pyqtSignal()
    """Emits an event when the currently viewed level is changed"""

    def __init__(self, name="Untitled"):
        """Constructor.
        :param name: The name of the Map, set to "Untitled" by default
        :type name: str
        """
        super().__init__()
        self.layers = None
        self.name = name
        # Set the Map's CRS to EPSG:3857 for display purposes
        self.crs = constants.EPSG_3857

    def new_map(self, name, layers):
        """Creates a new Map.
        :param name: The name of the new Map
        :type name: str
        :param layers: a array containing layers for the new Map
        :type layers: list
        """
        self.name = name
        self.layers = layers
        # Connected the levels_changed signal of the rooms layer
        # to the levels_changed signal of the Map
        self.layers['rooms'].levels_changed.connect(
          lambda: self.levels_changed.emit()
        )
        # Emit the map_created signal
        self.map_created.emit()

    def get_name(self):
        """Getter for name property
        
        :returns: The Map's name.
        :rtype: str
        """
        return self.name

    def get_buildings(self, bbox=None):
        """Returns all of the buildings in the Map.
        :param bbox: The area containing the buildings,
            the default is None (the whole map) 
        :type name: QgsRectangle

        :note: The building objects are created new everytime this method is
            called. You should not store this value as it will not be updated
            if the map is changed.

        :returns: A list of buildings
        :rtype: list
        """
        if self.layers is None:
            return []

        layer = self.layers['buildings']
        floors_layer = self.layers['rooms']
        lm_layer = self.layers['landmarks']

        buildings = [Building(b, layer.fields) for b in layer.get_features(bbox=bbox)]

        for building in buildings:
            box = building.get_bounding_box()
            floor_nos = floors_layer.get_levels(box)
            floors = [Floor(f, floors_layer) for f in floor_nos]
            building.add_floors(floors)
            for floor in floors:
                query = '"level" = \'{}\''.format(floor.get_number())
                rooms = [Room(r, floors_layer.fields) for r in floors_layer.get_features(query=query, bbox=box)]
                floor.add_rooms(rooms)
                query += ' and "indoor" = \'yes\''
                landmarks = [Landmark(l, lm_layer.fields) for l in lm_layer.get_features(query=query, bbox=box)]
                floor.add_landmarks(landmarks)

        return buildings

    def get_landmarks(self):
        layer = self.layers['landmarks']
        query = '"indoor" = \'no\''
        return [Landmark(f, layer.fields) for f in layer.get_features(query=query)]

    def get_paths(self):
        layer = self.layers['paths']
        return [Path(layer, f) for f in layer.get_features()]

    def get_layers(self):
        return self.layers

    def add_feature(self, layer, fields, geom):
        return self.layers[layer].add_feature(fields, geom)

    def set_crs(self, crs):
        self.crs = crs
        for name, layer in self.layers.items():
            layer.set_crs(crs)

    def get_crs(self):
        return self.crs