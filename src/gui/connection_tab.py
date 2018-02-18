from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from src.gui.fileexplorer import FileExplorer


class ConnectionTab(FloatLayout):
    def __init__(self):
        super(ConnectionTab, self).__init__()
        self.add_widget(FileExplorer())
