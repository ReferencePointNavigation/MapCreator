from enum import Enum


class Rewards(Enum):
    """
    Defines the reward for a particular action
    """
    MOVEMENT = -1
    BAD_MOVE = -5
    EXIT = 100
