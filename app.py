from kivy.app import App
from gui.main_window import MainWindow


class SEASideApp(App):
    def build(self):
        return MainWindow()
