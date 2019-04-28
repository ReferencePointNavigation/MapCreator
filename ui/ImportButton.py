from .UIInterface import UIInterface
from PyQt5.QtWidgets import QFileDialog


class ImportButton(UIInterface):

    def __init__(self, plugin):
        super().__init__(plugin)

        self.plugin.add_action(
            self.plugin.resource_path + 'import.svg',
            text=self.plugin.tr(u'Import Reference Point Map'),
            callback=self.open_import,
            parent=self.plugin.iface.mainWindow())

    def open_import(self):
        qfd = QFileDialog()
        title = 'Open File'
        f = QFileDialog.getOpenFileName(qfd, title, "~")
        if len(f[0]) > 2:
            parseProtobuf(f[0])
