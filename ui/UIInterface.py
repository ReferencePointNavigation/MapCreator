
class UIInterfaceMeta(type):
    def __init__(cls, name, bases, dct):
        super(UIInterfaceMeta, cls).__init__(name, bases, dct)
        if not hasattr(cls, 'registry'):
            cls.registry = set()
        cls.registry.add(cls)
        #cls.registry -= set(bases)

    def __iter__(cls):
        return iter(cls.registry)

    def __str__(cls):
        if cls in cls.registry:
            return cls.__name__
        return cls.__name__ + ": " + ", ".join([sc.__name__ for sc in cls])


class UIInterface(metaclass=UIInterfaceMeta):

    def __init__(self, plugin):
        self.plugin = plugin

    @staticmethod
    def get_ui_elements(plugin):
        return [element(plugin) for element in UIInterface]

