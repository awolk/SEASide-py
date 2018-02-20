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

from PyQt5.QtWidgets import QWidget
from gui.loader import Loader
from gui.login import Login
from gui.connection_tab import ConnectionTab
from connection import Connection

class MasterTab(QWidget):
    def __init__(self, server, config):
        super(MasterTab, self).__init__()