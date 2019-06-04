from PyQt5.QtCore import pyqtSignal, QObject


class Elvis(QObject):

    map_created = pyqtSignal()

    def __init__(self, mmap):
        super().__init__()
        self.map = mmap
        self.map.map_created.connect(lambda: self.map_created.emit())

    def get_buildings(self):
        return self.map.get_buildings()

    def get_landmarks(self):
        return self.map.get_landmarks()

