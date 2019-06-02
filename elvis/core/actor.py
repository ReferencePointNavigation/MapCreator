

class Actor(object):

    def __init__(self, position, stride=1.0):
        self.terminal_state = False
        self.position = position.copy()
        self.stride = stride

    def set_position(self, position):
        self.position = position.copy()

    def get_position(self):
        return self.position

    def set_terminal_state(self, state):
        self.terminal_state = state

    def in_terminal_state(self):
        return self.terminal_state

    def reset(self, position):
        self.set_position(position)
        self.terminal_state = False
