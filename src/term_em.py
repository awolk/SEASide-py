import pyte
from pyte import control as ctrl, escape as esc
from PyQt5.Qt import QApplication


class TerminalEmulator:
    def __init__(self, connection):
        self._connection = connection
        self._screen = pyte.Screen(80, 24)
        self._screen.bell = self._beep
        self._stream = pyte.ByteStream(self._screen)

    def write(self, in_bytes):
        """Write bytes from client to server"""
        self._connection.send_ssh_bytes(in_bytes)

    def _beep(self, *args):
        QApplication.instance().beep()

    def receive(self):
        """Receive bytes from server"""
        if self._connection.has_ssh_data():
            self._stream.feed(self._connection.receive_ssh_data())

    def resize(self, rows=24, cols=80):
        self._connection.resize_term(rows, cols)
        self._screen.resize(rows, cols)

    def get_cursor(self):
        return self._screen.cursor.x, self._screen.cursor.y

    def dirty_lines(self):
        return self._screen.dirty

    def clear_dirty(self):
        self._screen.dirty.clear()

    def get_text(self):
        return '\n'.join(self._screen.display)

    def get_line(self, n):
        if n < len(self._screen.display):
            return self._screen.display[n]
        return ''

    def _cursor_ecape_char(self):
        DECCKM = 1 << 5
        return 'O' if DECCKM in self._screen.mode else '['

    def key_up(self):
        cursor_escape = self._cursor_ecape_char()
        self.write(ctrl.ESC + cursor_escape + esc.CUU)

    def key_down(self):
        cursor_escape = self._cursor_ecape_char()
        self.write(ctrl.ESC + cursor_escape + esc.CUD)

    def key_left(self):
        cursor_escape = self._cursor_ecape_char()
        self.write(ctrl.ESC + cursor_escape + esc.CUB)

    def key_right(self):
        cursor_escape = self._cursor_ecape_char()
        self.write(ctrl.ESC + cursor_escape + esc.CUF)

    def open_connection(self):
        return self._connection.has_open_connection()
