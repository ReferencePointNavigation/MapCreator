from enum import Enum


class FunctionProxy:
    """
    Utility class which allows an Enum to be used as a
    dispatch table
    """
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)



class Actions(Enum):
    """
    The allowable actions
    """
    ACTION_UP = FunctionProxy(lambda p: p.up())
    ACTION_RIGHT = FunctionProxy(lambda p: p.right())
    ACTION_DOWN = FunctionProxy(lambda p: p.down())
    ACTION_LEFT = FunctionProxy(lambda p: p.left())

    def __repr__(self):
        """
        The string representation of the action
        Necessary because functions have no string representation
        :return: the enum member's name
        """
        return '<%s.%s>' % (self.__class__.__name__, self.name)

    def __deepcopy__(self, memo):
        return self
