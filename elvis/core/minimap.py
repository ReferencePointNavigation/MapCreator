from .states import States


class MiniMap:

    def __init__(self, tiles, height, width, start, end):
        self.tiles = tiles
        self.height = height
        self.width = width
        self.start = start
        self.end = end

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_start_position(self):
        return self.start

    def get_end_position(self):
        return self.end

    def __getitem__(self, key):
        return self.tiles[key]

    def get_content(self, position):
        return self.tiles[position.y][position.x]

    def set_content(self, position, content):
        self.tiles[position.y][position.x] = content

    def print(self):
        for row in self.tiles[::-1]:
            for column in row:
                if column is States.EMPTY:
                    print('.', end="")
                elif column is States.BLOCKED:
                    print('█', end="")
                elif column is States.ACTOR:
                    print('웃', end="")
                elif column is States.END:
                    print('X', end="")
                elif column is States.LANDMARK:
                    print('L', end="")
            print()

    def reset(self):
        #self.set_content(self.start, States.ACTOR)
        self.set_content(self.end, States.END)