from .actions import Actions
from .rewards import Rewards
from .states import States


class Environment:

    def __init__(self, minimap, actor):
        self.grid = minimap
        self.actor = actor
        self.height = minimap.get_height()
        self.width = minimap.get_width()

    def actor_in_terminal_state(self):
        return self.actor.in_terminal_state()

    def get_actor_state(self):
        return self.actor.get_state()

    def __position_on_grid(self, pos):
        return (0 <= pos.x < self.width) and (0 <= pos.y < self.height)

    def perform_action(self, action):
        reward = 0

        actor_requested_pos = self.actor.get_position().copy()

        if action == Actions.ACTION_UP:
            actor_requested_pos.up()

        elif action == Actions.ACTION_RIGHT:
            actor_requested_pos.right()

        elif action == Actions.ACTION_DOWN:
            actor_requested_pos.down()

        elif action == Actions.ACTION_LEFT:
            actor_requested_pos.left()

        else:
            assert False, 'action=' + str(action)

        if self.__position_on_grid(actor_requested_pos):
            requested_location_contents = self.grid[actor_requested_pos.y][actor_requested_pos.x]
        else:
            requested_location_contents = States.BLOCKED

        def move_actor_to_requested_location():
            self.grid[self.actor_pos.y][self.actor_pos.x] = States.EMPTY
            self.actor_pos = actor_requested_pos
            self.grid[self.actor_pos.y][self.actor_pos.x] = States.ACTOR

        if requested_location_contents == States.BLOCKED:
            reward += Rewards.BAD_MOVE.value

        elif requested_location_contents == States.EMPTY:
            reward += Rewards.MOVEMENT
            move_actor_to_requested_location()

        elif requested_location_contents == States.EXIT:
            reward += Rewards.MOVEMENT + Rewards.EXIT
            move_actor_to_requested_location()
            self.actor.set_terminal_state(True)
            print("SUCCESS")

        else:
            assert False, 'requested_location_contents=' + str(requested_location_contents)

        self.__update_environment()

        return reward

    def __update_environment(self):
        pass