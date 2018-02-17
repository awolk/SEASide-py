from kivy.uix.floatlayout import FloatLayout
from src.gui.loader import Loader
from src.gui.login import Login

# Stub
class Connection:
    def __init__(self, *args, **kwargs): ...


class MasterTab(FloatLayout):
    def __init__(self, server):
        super(MasterTab, self).__init__()
        self._connection = Connection(server)
        self._loader = Loader()
        self.add_widget(self._loader)
        self._loader.force_fail()

    def get_connection(self):
        return self.connection

    def connection_failed(self):
        self.remove_widget(self._loader)
        self._login = Login('Sample Message')
        self.add_widget(self._login)

    def give_credentials(self):
        ...
