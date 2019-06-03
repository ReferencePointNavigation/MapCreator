from .rewards import Rewards
from .states import States


class Environment:
    """
    Defines the environment in which the learning takes place
    """
    def __init__(self, grid, actor):
        """
        Initializes a new Environment
        :param grid: a MiniMap grid of the environment
        :param actor: the primary actor
        """
        self.grid = grid
        self.actor = actor
        self.height = grid.get_height()
        self.width = grid.get_width()
        self.prev_value = States.LANDMARK

    def get(self):
        return self.grid.tiles[::-1]

    def actor_in_terminal_state(self):
        return self.actor.in_terminal_state()

    def get_actor_state(self):
        return self.actor.get_position()

    def perform_action(self, action):

        reward = 0
        requested_location_contents = States.BLOCKED

        actor_requested_pos = self.actor.get_position().copy()

        action.value(actor_requested_pos)

        if self.__position_on_grid(actor_requested_pos):
            requested_location_contents = self.grid.get_content(actor_requested_pos)

        def move_actor_to_requested_location():
            actor_pos = self.actor.get_position()
            self.grid.set_content(actor_pos, self.prev_value)
            self.actor.set_position(actor_requested_pos)
            self.prev_value = self.grid.get_content(actor_requested_pos)
            self.grid.set_content(actor_requested_pos, States.ACTOR)

        if requested_location_contents == States.BLOCKED:
            reward += Rewards.BAD_MOVE.value

        elif requested_location_contents == States.EMPTY:
            reward += Rewards.MOVEMENT.value
            move_actor_to_requested_location()

        elif requested_location_contents == States.END:
            reward += Rewards.MOVEMENT.value + Rewards.EXIT.value
            move_actor_to_requested_location()
            self.actor.set_terminal_state(True)
            print("SUCCESS")

        elif requested_location_contents == States.LANDMARK:
            reward += Rewards.MOVEMENT.value
            move_actor_to_requested_location()

        else:
            assert False, 'requested_location_contents=' + str(requested_location_contents)

        self.__update_environment()

        return reward

    def __position_on_grid(self, pos):
        return (0 <= pos.x < self.width) and (0 <= pos.y < self.height)

    def __update_environment(self):
        pass

    def reset(self):
        self.grid.set_content(self.actor.get_position(), States.EMPTY)
        self.actor.reset(self.grid.get_start_position())
        self.prev_value = States.LANDMARK
        self.grid.reset()
