from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from gui.loader import Loader
from gui.login import Login
from gui.connection_tab import ConnectionTab
from connection import Connection


class MasterTab(QWidget):
    def __init__(self, server, config):
        super(MasterTab, self).__init__()
        self._connection = Connection(server)
        self._config = config
        # Build GUI
        self._loader = Loader(self)
        self._login = None
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._loader, Qt.AlignCenter)
        self.setLayout(self._layout)
        # TODO: This should be a separate thread
        self._loader.connect(config.get_username())

    def get_connection(self):
        return self._connection

    def connection_failed(self, error=''):
        self._layout.removeWidget(self._loader)  # Remove Loader
        self._loader.deleteLater()
        self._login = Login(self)                # Add Login
        self._login.update_error(error)
        self._layout.addWidget(self._login)

    def give_credentials(self, username, password):
        self._layout.removeWidget(self._login)  # Remove Login
        self._login.deleteLater()
        self._loader = Loader(self)             # Add Loader
        self._layout.addWidget(self._loader)
        QTimer.singleShot(0, lambda: self._loader.connect(username, password))

    def connection_successful(self, username):
        self._layout.removeWidget(self._loader)  # Remove Loader
        self._loader.deleteLater()
        display = ConnectionTab()          # Add Connection Tab
        self._layout.addWidget(display)
        self._config.set_username(username)
        display.start()
