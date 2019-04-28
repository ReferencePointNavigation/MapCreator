from .UIInterface import UIInterface
from PyQt5.QtWidgets import QFileDialog
from qgis.core import QgsProject


class ExportButton(UIInterface):

    def __init__(self, plugin):
        super().__init__(plugin)

        self.plugin.add_action(
            self.plugin.resource_path + 'export.svg',
            text=self.plugin.tr(u'Export Reference Point Map'),
            callback=self.open_export,
            parent=self.plugin.iface.mainWindow())

    def open_export(self):
        qfd = QFileDialog()
        qfd.setFileMode(QFileDialog.DirectoryOnly)
        title = 'Select Directory'
        if qfd.exec_() == QDialog.Accepted:
            layers = [layer for name, layer in QgsProject.instance().mapLayers().items() if type(layer) == QgsVectorLayer]
            exporter = RPNMap()
            exporter.export_map(layers, qfd.selectedFiles()[0])
