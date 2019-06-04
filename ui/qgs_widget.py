from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QFileDialog, QAction, QDialog
from pubsub import pub


class QgsWidget(QAction):

    RESOURCE_PATH = ':/plugins/map_builder/resources/'

    registry = {}

    def __init__(self, iface, controller, icon, text):
        QAction.__init__(self,
                         QIcon(self.get_resource(icon)),
                         self.translate(text),
                         iface.mainWindow())
        self.iface = iface
        self.controller = controller
        self.triggered.connect(self.action)

    def get_resource(self, name):
        return self.RESOURCE_PATH + name + '.svg'

    # noinspection PyMethodMayBeStatic
    def translate(self, text):
        return text

    def action(self):
        pass


class FileManagerMixin:

    # noinspection PyMethodMayBeStatic
    def show_open_dialog(self, title):
        qfd = QFileDialog()
        f = QFileDialog.getOpenFileName(qfd, title, '~')
        return f[0]

    # noinspection PyMethodMayBeStatic
    def show_input_dialog(self, iface, title, prompt):
        text, _ = QInputDialog.getText(iface.mainWindow(), title, prompt, QLineEdit.Normal, '')
        return text

    # noinspection PyMethodMayBeStatic
    def show_save_folder_dialog(self, title):
        qfd = QFileDialog()
        qfd.setFileMode(QFileDialog.DirectoryOnly)
        if qfd.exec_() == QDialog.Accepted:
            return qfd.selectedFiles()[0]
        else:
            return None

