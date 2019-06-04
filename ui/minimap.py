from PyQt5.QtGui import QPainter, QPen, QColor
from qgis.gui import QgsMapCanvasItem
from qgis.core import QgsProject, QgsCoordinateTransform, QgsCoordinateReferenceSystem, QgsPointXY, QgsRectangle


class MiniMap(QgsMapCanvasItem):

    def __init__(self, canvas, mmap, tile_size=1.0):
        self.canvas = canvas
        QgsMapCanvasItem.__init__(self, canvas)
        self.setVisible(False)
        self.map = mmap
        self.tile_size = tile_size
        self.level = 0
        self.grid_pen = QPen(QColor(127, 127, 127, 120))
        self.transformer = QgsCoordinateTransform(
            self.canvas.mapSettings().destinationCrs(),
            QgsCoordinateReferenceSystem(self.map.get_crs()),
            QgsProject.instance())
        self.grid = []

        self.canvas.extentsChanged.connect(self.on_extents_changed)

    def on_extents_changed(self):
        self.refresh()

    def refresh(self):
        if self.isVisible():
            self.build_grid()
        self.updateCanvas()

    def on_show_minimap(self, arg1):
        self.set_enabled(arg1)

    def set_enabled(self, enabled):
        self.setVisible(enabled)
        self.refresh()

    def set_level(self, level):
        self.level = level
        self.refresh()

    def build_grid(self):
        if self.map.get_layers() is None:
            return

        extent = self.canvas.extent()
        grid = []
        for building in self.map.get_buildings(bbox=extent):
            floor = building.get_floor(self.level)
            if floor is not None:
                grid += floor.get_grid()

        self.grid = []
        for tile in grid:
            canvas_pt = self.toCanvasCoordinates(QgsPointXY(tile[3][0], tile[3][1]))
            canvas_pt_max = self.toCanvasCoordinates(QgsPointXY(tile[1][0], tile[1][1]))
            self.grid.append((canvas_pt.x(), canvas_pt.y(), canvas_pt_max.x() - canvas_pt.x(),
                             canvas_pt_max.y() - canvas_pt.y()))

    def paint(self, painter, option=None, widget=None):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Difference)

        scale_factor = painter.fontMetrics().xHeight() / 4

        if scale_factor < 1.0:
            return

        self.grid_pen.setWidth(int(scale_factor))

        painter.setPen(self.grid_pen)

        for tile in self.grid:
            painter.drawRect(tile[0], tile[1], tile[2], tile[3])

        painter.restore()
