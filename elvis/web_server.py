import json
import os

from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from urllib.parse import unquote
from elvis.core import States


TCPServer.allow_reuse_address = True

PUBLIC_ENUMS = {
    'States': States
}


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) in PUBLIC_ENUMS.values():
            return str(obj)
        return str(obj) #json.JSONEncoder.default(self, obj)


def as_enum(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(PUBLIC_ENUMS[name], member)
    else:
        return d


class ElvisRequestHandler(SimpleHTTPRequestHandler):

    environment = None
    strategy = None

    def do_GET(self):
        MOVE_PREFIX = '/move/'
        dir_path = os.path.dirname(os.path.realpath(__file__))

        if self.path == '/init':
            config_file = os.path.join(dir_path, 'default.json')
            config = None
            with open(config_file, 'r') as f:
                config = json.load(f)
            ElvisRequestHandler.strategy.new_episode()
            ElvisRequestHandler.environment.reset()
            return self.__send_json(ElvisRequestHandler.environment.get())

        elif self.path == '/':
            self.path = 'elvis/web/index.html'

        elif self.path.startswith(MOVE_PREFIX):
            state_before = ElvisRequestHandler.environment.get_actor_state()
            action = ElvisRequestHandler.strategy.next_action(state_before)
            reward = ElvisRequestHandler.environment.perform_action(action)
            state_after = ElvisRequestHandler.environment.get_actor_state()
            ElvisRequestHandler.strategy.update(state_before, action, reward, state_after)

            response = {
                'env' : ElvisRequestHandler.environment.get(),
                'terminal' : ElvisRequestHandler.environment.actor_in_terminal_state(),
                'stats' : {
                    'ε' : ElvisRequestHandler.strategy.e,
                    'episode' : ElvisRequestHandler.strategy.episode
                }
            }

            return self.__send_json(response)

        else:
            self.path = 'elvis/' + self.path

        return SimpleHTTPRequestHandler.do_GET(self)

    def __send_json(self, obj):
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(obj, cls=EnumEncoder), 'utf-8'))


