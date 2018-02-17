from kivy.app import App
from src.gui.main_window import MainWindow


class SEASideApp(App):
    def build(self):
        return MainWindow()
