# from kivy.uix.floatlayout import FloatLayout
# from gui.fileexplorer import FileExplorer
# from gui.terminal import Terminal
#
#
# class ConnectionTab(FloatLayout):
#     def __init__(self):
#         super(ConnectionTab, self).__init__()
#         self._file_explorer = FileExplorer(
#             size_hint=(0.25, 1),
#             pos_hint={'left': 0}
#         )
#         self._term = Terminal(
#             size_hint=(0.75, 1),
#             pos_hint={'right': 1}
#         )
#         self.add_widget(self._file_explorer)
#         self.add_widget(self._term)
#
#     def start(self):
#         self._term.start()
#         self._file_explorer.start(self.get_connection().get_home_dir())
#
#     def get_connection(self):
#         return self.parent.get_connection()

from PyQt5.QtWidgets import QWidget, QHBoxLayout
from gui.fileexplorer import FileExplorer
from gui.terminal import Terminal


class ConnectionTab(QWidget):
    def __init__(self):
        super(ConnectionTab, self).__init__()
        self._layout = QHBoxLayout()
        self._file_explorer = FileExplorer(self)
        self._term = Terminal(self)
        self._layout.addWidget(self._file_explorer)
        self._layout.addWidget(self._term)
        self.setLayout(self._layout)

    def start(self):
        self._term.start()
        self._file_explorer.start(self.get_connection().get_home_dir())

    def get_connection(self):
        return self.parent().get_connection()
