
class Position:
    def __init__(self, x, y, stride=1.0):
        self.x = x
        self.y = y
        self.stride = stride

    def dist_sq(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def copy(self):
        return Position(self.x, self.y, self.stride)

    def up(self):
        self.y -= self.stride

    def down(self):
        self.y += self.stride

    def left(self):
        self.x -= self.stride

    def right(self):
        self.x += self.stride

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '{},{}'.format(self.x, self.y)