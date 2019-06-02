import sys
import signal
import getopt
import json
import os
from socketserver import TCPServer

from .web_server import ElvisRequestHandler

from elvis.core import (
    Simulation,
    Strategy,
    Actor,
    Environment)

from .utils import MapReader



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
    runweb = False

    try:
        opts, args = getopt.getopt(argv, "h:c:w", ["config=", "web",""])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-c", "--config"):
            config_file = arg
        elif opt in ("-w", "--web"):
            runweb = True

    signal.signal(signal.SIGINT, save_and_exit)

    with open(config_file, 'r') as f:
        config = json.load(f)

    if config is None:
        print('The was an error loading the config file {0}'.format(config_file))
        exit(2)

    strategy = build_strategy()
    reader = MapReader(config)
    grid = reader.build_map()
    actor = Actor(grid.get_start_position())
    environment = Environment(grid, actor)

    if runweb:
        ElvisRequestHandler.environment = environment
        ElvisRequestHandler.strategy = strategy
        Handler = ElvisRequestHandler
        server = TCPServer(('0.0.0.0', 8080), Handler)
        server.serve_forever()
    else:
        simulation = Simulation(config, actor, strategy, environment)
        simulation.run()


if __name__ == '__main__':
    main(sys.argv[1:])

