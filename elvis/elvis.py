from pubsub import pub


class Elvis:

    def __init__(self, mmap):
        self.map = mmap

    def get_buildings(self):
        return self.map.get_buildings()

    def get_landmarks(self):
        return self.map.get_landmarks()

    # noinspection PyMethodMayBeStatic
    def publish(self, topic, arg1):
        pub.sendMessage(topic.value, arg1=arg1)

    # noinspection PyMethodMayBeStatic
    def subscribe(self, listener, topic):
        pub.subscribe(listener, topic.value)
