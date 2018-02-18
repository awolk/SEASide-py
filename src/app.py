from kivy.app import App
from kivy.config import Config

from src.gui.main_window import MainWindow

Config.set('kivy', 'exit_on_escape', 0)
Config.set('graphics', 'resizable', 0)

class SEASideApp(App):
    def build(self):
        return MainWindow()
