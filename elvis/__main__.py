import sys
import signal
import getopt
import json
import os

from elvis.core import (
    Simulation,
    Strategy,
    Actor,
    Environment,
    MiniMap)


def print_help():
    print('__main__.py -m <map> -c <episode_count> -i <save_interval>')


def save_and_exit(_1,_2):
    sys.exit(0)


def build_strategy():
    y = 0.99
    a = 0.1
    l = 0.1
    e = 0.1
    e_decay = 1
    return Strategy(y, a, l, e, e_decay)


def main(argv):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(dir_path, 'default.json')
    config = None

    try:
        opts, args = getopt.getopt(argv, "h:c:", ["config="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-c", "--config"):
            config_file = arg

    signal.signal(signal.SIGINT, save_and_exit)

    with open(config_file, 'r') as f:
        config = json.load(f)

    if config is None:
        print('The was an error loading the config file {0}'.format(config_file))
        exit(2)

    strategy = build_strategy()

    grid = MiniMap(config)
    actor = Actor()
    environment = Environment(grid, actor)
    simulation = Simulation(config, actor, strategy, environment)

    simulation.run()


if __name__ == '__main__':
    main(sys.argv[1:])

