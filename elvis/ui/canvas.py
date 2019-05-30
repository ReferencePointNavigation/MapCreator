from qgis.gui import QgsMapCanvasItem


class Canvas(QgsMapCanvasItem):

    def __init__(self, canvas, mmap, tile_size):
        self.canvas = canvas
        QgsMapCanvasItem.__init__(self, canvas)
        self.enabled = False

    def paint(self, painter, option=None, widget=None):
        if not self.enabled:
            return

