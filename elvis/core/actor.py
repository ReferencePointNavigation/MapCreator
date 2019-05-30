from .position import Position


class Actor(object):

    def __init__(self):
        self.terminal_state = False
        self.position = Position(0,0)

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def get_state(self):
        pass

    def set_terminal_state(self, state):
        self.terminal_state = state

    def in_terminal_state(self):
        return self.terminal_state

    def perform_action(self, action):
        pass