from kivy.uix.floatlayout import FloatLayout
from src.gui.loader import Loader
from src.gui.login import Login
from src.gui.connection_tab import ConnectionTab
from src.connection import Connection


class MasterTab(FloatLayout):
    def __init__(self, server, username):
        super(MasterTab, self).__init__()
        self._username = username
        self._connection = Connection(server)
        self._loader = Loader()
        self._login = Login()
        self._display = ConnectionTab()
        self.add_widget(self._loader)
        self._loader.connect(self._username)

    def get_connection(self):
        return self._connection

    def connection_failed(self):
        self.clear_widgets()
        self.add_widget(self._login)

    def give_credentials(self, username, password=None):
        self.clear_widgets()
        self.add_widget(self._loader)
        self._loader.connect(username, password)

    def connection_successful(self):
        self.clear_widgets()
        self.add_widget(self._display)