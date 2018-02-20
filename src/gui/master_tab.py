# from kivy.uix.floatlayout import FloatLayout
# from gui.loader import Loader
# from gui.login import Login
# from gui.connection_tab import ConnectionTab
# from connection import Connection
# from kivy.clock import Clock
#
#
# class MasterTab(FloatLayout):
#     def __init__(self, server, config):
#         super(MasterTab, self).__init__()
#         self._connection = Connection(server)
#         self._loader = Loader()
#         self._login = Login()
#         self._display = ConnectionTab()
#         self.add_widget(self._loader)
#         self._config = config
#         Clock.schedule_once(lambda dt: self._loader.connect(config.get_username()), 0)
#
#     def get_connection(self):
#         return self._connection
#
#     def connection_failed(self, error=''):
#         self.clear_widgets()
#         self._login.update_error(error)
#         self.add_widget(self._login)
#
#     def give_credentials(self, username, password):
#         self.clear_widgets()
#         self.add_widget(self._loader)
#         self._config.set_username(username)
#         Clock.schedule_once(lambda dt: self._loader.connect(username, password), 0)
#
#     def connection_successful(self):
#         self.clear_widgets()
#         self.add_widget(self._display)
#         self._display.start()

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
        QTimer.singleShot(0, lambda: self._loader.connect(config.get_username()))

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
