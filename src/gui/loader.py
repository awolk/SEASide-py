from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class Loader(QLabel):
    def __init__(self, parent):
        self._parent = parent
        super(Loader, self).__init__('Loading...')
        self.setAlignment(Qt.AlignHCenter)

    def connect(self, username=None, password=None):
        if username is None:
            return self._parent.connection_failed()
        conn = self._parent.get_connection()
        success = conn.attempt_login(username, password) if password else conn.attempt_connection(username)
        if success:
            self._parent.connection_successful(username)
        else:
            self._parent.connection_failed('Login failed')