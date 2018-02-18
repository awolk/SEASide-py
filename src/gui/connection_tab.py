from kivy.uix.floatlayout import FloatLayout
from src.gui.fileexplorer import FileExplorer
from src.gui.terminal import Terminal


class ConnectionTab(FloatLayout):
    def __init__(self):
        super(ConnectionTab, self).__init__()
        self.add_widget(FileExplorer(
            size_hint=(0.25, 1),
            pos_hint={'left': 0}
        ))
        self._term = Terminal(
            size_hint=(0.75, 1),
            pos_hint={'right': 1}
        )
        self.add_widget(self._term)

    def start(self):
        self._term.start()

    def get_connection(self):
        return self.parent.get_connection()