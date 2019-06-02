from enum import Enum


class FunctionProxy:

    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class Actions(Enum):
    ACTION_UP = FunctionProxy(lambda p: p.up())
    ACTION_RIGHT = FunctionProxy(lambda p: p.right())
    ACTION_DOWN = FunctionProxy(lambda p: p.down())
    ACTION_LEFT = FunctionProxy(lambda p: p.left())

    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)
