import sys
import signal
import getopt

from elvis.strategy import Strategy
from elvis.environment import Environment
from elvis.actor import Actor

from ui import QgsMap, LayerFactory

MAX_EPISODE_STEPS = 100000

def build_strategy():
    y = 0.99
    a = 0.1
    l = 0.1
    e = 0.1
    e_decay = 1
    return Strategy(y, a, l, e, e_decay)


def build_environment(mmap, actor):
    return Environment(mmap, actor)


def run_episode(strategy):

    mmap = QgsMap(u'Untitled', LayerFactory())

    actor = Actor()
    environment = build_environment(mmap, actor)
    steps = 0
    total_reward = 0

    strategy.new_episode()

    while not actor.in_terminal_state() and steps < MAX_EPISODE_STEPS:
        state_before = actor.get_state()
        action = strategy.next_action(state_before)
        reward = actor.perform_action(action)
        state_after = actor.get_state()
        strategy.update(state_before, action, reward, state_after)
        total_reward += reward
        steps += 1

    return steps, total_reward


def save_to_file(strategy):
    pass


def save_and_exit(_1,_2):
    sys.exit(0)


def main(argv):

    episode_count = 1000 * 1000
    save_interval = 100

    try:
        opts, args = getopt.getopt(argv, "hc:i:", ["count=", "interval="])
    except getopt.GetoptError:
        print('main.py -c <episode_count> -i <save_interval>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -c <episode_count> -i <save_interval>')
            sys.exit()
        elif opt in ("-c", "--count"):
            episode_count = arg
        elif opt in ("-i", "--interval"):
            save_interval = arg

    signal.signal(signal.SIGINT, save_and_exit) # handle ctrl-c
    strategy = build_strategy()

    for episode_index in range(episode_count):
        run_episode(strategy)
        if episode_index > 0 and episode_index % save_interval == 0:
            save_to_file(strategy)
            print(episode_index)


if __name__ == '__main__':
    main(sys.argv[1:])

