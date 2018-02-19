import appdirs
import pathlib
from configparser import ConfigParser
import os
import server_config

_data_dir = appdirs.user_data_dir('SEASide')
_data_file = os.path.join(_data_dir, 'SEASide_config.ini')

pathlib.Path(_data_dir).mkdir(parents=True, exist_ok=True)


class Configuration:
    def __init__(self):
        self._parser = ConfigParser()
        self._parser.read(_data_file)

    def get_username(self):
        return self._parser.get('info', 'username', fallback=None)

    def get_default_server(self):
        return self._parser.get('info', 'server', fallback=server_config.DEFAULT_SERVER)

    def _write(self, section, key, value):
        if not self._parser.has_section(section):
            self._parser.add_section(section)
        self._parser.set(section, key, value)
        with open(_data_file, 'w') as file:
            self._parser.write(file)

    def set_username(self, username):
        self._write('info', 'username', username)

    def set_default_server(self, server):
        if server in server_config.SERVERS.keys():
            self._write('info', 'sever', server)
        else:
            raise Exception('Invalid server specified')
