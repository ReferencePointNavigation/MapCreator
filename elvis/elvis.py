

class Elvis:

    def __init__(self, mmap):
        self.map = mmap

    def get_buildings(self):
        return self.map.get_buildings()

    def get_landmarks(self):
        return self.map.get_landmarks()

