from PyQt5.QtGui import QPainter, QPen, QColor
from qgis.gui import QgsMapCanvasItem
from qgis.core import QgsProject, QgsCoordinateTransform, QgsCoordinateReferenceSystem, QgsPointXY, qgsDoubleNear, QgsMessageLog
from math import ceil
from pubsub import pub
from referencepoint.topics import Topics

class MiniMap(QgsMapCanvasItem):

    def __init__(self, canvas, mmap, tile_size):
        self.canvas = canvas
        QgsMapCanvasItem.__init__(self, canvas)
        self.enabled = False
        self.map = mmap
        self.tile_size = tile_size
        self.level = 0
        self.grid_pen = QPen(QColor(127, 127, 127, 120))
        self.transformer = QgsCoordinateTransform(
            self.canvas.mapSettings().destinationCrs(),
            QgsCoordinateReferenceSystem(self.map.get_crs()),
            QgsProject.instance())
        pub.subscribe(self.on_show_minimap, Topics.SHOW_MINIMAP.value)
        pub.subscribe(self.on_level_selected, Topics.LEVEL_SELECTED.value)

    def on_level_selected(self, arg1):
        if arg1 is not None:
            self.set_level(int(arg1))

    def on_show_minimap(self, arg1):
        self.set_enabled(arg1)

    def set_enabled(self, enabled):
        self.enabled = enabled
        self.canvas.refresh()

    def set_level(self, level):
        self.level = level

    def paint(self, painter, option=None, widget=None):
        if not self.enabled:
            return

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_Difference)

        scale_factor = painter.fontMetrics().xHeight() / 4
        self.grid_pen.setWidth(int(scale_factor))
        painter.setPen(self.grid_pen)

        for building in self.map.get_buildings(bbox=self.canvas.extent()):
            floor = building.get_floor(self.level)
            if floor is not None:
                bbox = floor.get_bounding_box()
                min_x = bbox.xMinimum()
                min_y = bbox.yMinimum()
                max_x = bbox.xMaximum()
                max_y = bbox.yMaximum()
                rows = max(ceil((max_y - min_y) / self.tile_size), 0)
                columns = max(ceil((max_x - min_x) / self.tile_size), 0)
                curr_y = min_y
                curr_x = min_x
                for i in range(0, rows):
                    for column in range(0, columns):
                        tile = [
                            (curr_x, curr_y),
                            (curr_x + self.tile_size, curr_y),
                            (curr_x + self.tile_size, curr_y + self.tile_size),
                            (curr_x, curr_y + self.tile_size)
                        ]
                        if floor.intersects(tile):
                            canvas_pt = self.toCanvasCoordinates(QgsPointXY(tile[3][0], tile[3][1]))
                            canvas_pt_max = self.toCanvasCoordinates(QgsPointXY(tile[1][0], tile[1][1]))
                            painter.drawRect(canvas_pt.x(), canvas_pt.y(), canvas_pt_max.x() - canvas_pt.x(), canvas_pt_max.y() - canvas_pt.y())
                        curr_x += self.tile_size
                    curr_x = min_x
                    curr_y += self.tile_size

        painter.restore()
