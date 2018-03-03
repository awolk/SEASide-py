from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot
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
        self._loader = self._build_loader()
        self._login = None
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._loader, Qt.AlignCenter)
        self.setLayout(self._layout)
        self._loader.connect(config.get_username())

    def get_connection(self):
        return self._connection

    def _build_loader(self):
        loader = Loader(self)
        loader.success.connect(self.connection_successful)
        loader.failure.connect(self.connection_failed)
        return loader

    @pyqtSlot(str)
    def connection_failed(self, error=''):
        self._layout.removeWidget(self._loader)  # Remove Loader
        self._loader.deleteLater()
        self._login = Login(self)                # Add Login
        self._login.update_error(error)
        self._layout.addWidget(self._login)

    def give_credentials(self, username, password):
        self._layout.removeWidget(self._login)  # Remove Login
        self._login.deleteLater()
        self._loader = self._build_loader()      # Add Loader
        self._layout.addWidget(self._loader)
        self._loader.connect(username, password)

    @pyqtSlot(str)
    def connection_successful(self, username):
        self._layout.removeWidget(self._loader)  # Remove Loader
        self._loader.deleteLater()
        display = ConnectionTab()                # Add Connection Tab
        self._layout.addWidget(display)
        self._config.set_username(username)
        display.start()
