import pyte
from kivy.metrics import dp, sp

class TerminalEmulator:
    def __init__(self, connection):
        self._connection = connection
        self._screen = pyte.Screen(int(sp(80)), int(sp(24)))
        self._stream = pyte.ByteStream(self._screen)

    def write(self, in_bytes):
        """Write bytes from client to server"""
        self._connection.send_ssh_bytes(in_bytes)

    def receive(self):
        """Receive bytes from server"""
        if self._connection.has_ssh_data():
            self._stream.feed(self._connection.receive_ssh_data())

    def resize(self, cols=sp(80), rows=sp(24)):
        self._screen.resize(cols, rows)
        self._connection.resize_term(cols, rows)

    def get_cursor(self):
        return self._screen.cursor.x, self._screen.cursor.y

    def is_dirty(self):
        return bool(self._screen.dirty)

    def clear_dirty(self):
        self._screen.dirty.clear()

    def get_text(self):
        return '\n'.join(self._screen.display)