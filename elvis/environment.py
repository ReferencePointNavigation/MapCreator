

class Environment:

    def __init__(self, map, actor):
        self.map = map
        self.actor = actor

    def get_actor_state(self):
        return self.actor.get_state()

