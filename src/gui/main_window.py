# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.spinner import Spinner
# from kivy.uix.button import Button
# from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
# from kivy.metrics import dp, sp
# from kivy.core.window import Window
#
# from gui.master_tab import MasterTab
# from server_config import SERVERS
# from savedata import Configuration
#
# class MainWindow(FloatLayout):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         Window.size = (1000, 560)
#         # Connection
#         self._config = Configuration()
#         server_names = tuple(sorted(SERVERS.keys()))
#         self._spinner = Spinner(
#             text=self._config.get_default_server(),
#             values=server_names,
#             size_hint=(None, None),
#             size=(dp(80), dp(60))
#         )
#         button = Button(
#             text='Connect',
#             size=(dp(80), dp(60)),
#             size_hint=(None, None)
#         )
#         button.bind(on_press=self._new_tab)
#         top_layout = BoxLayout(
#             spacing=dp(0),
#             orientation='horizontal',
#             pos_hint={'top': 1, 'right': 1},
#             size_hint=(None, None),
#             size=(dp(160), dp(55))
#         )
#         top_layout.add_widget(button)
#         top_layout.add_widget(self._spinner)
#         # Tab view
#         self._tab_view = TabbedPanel()
#         self._tab_view.default_tab_text = self._spinner.text
#         self._tab_view.default_tab_content = MasterTab(SERVERS[self._spinner.text], self._config)
#         # Build window
#         self.add_widget(top_layout)
#         self.add_widget(self._tab_view)
#
#     def _new_tab(self, *args):
#         server_name = self._spinner.text
#         server = SERVERS[server_name]
#         self._config.set_default_server(server_name)
#         header = TabbedPanelHeader(text=server_name)
#         header.content = MasterTab(server, self._config)
#         self._tab_view.add_widget(header)
#         self._tab_view.switch_to(header)
#
#     def get_username(self):
#         return self._config.get_username()

from PyQt5.QtWidgets import QMainWindow, QComboBox, QPushButton, QHBoxLayout, QWidget

#from gui.master_tab import MasterTab
from server_config import SERVERS
from savedata import Configuration


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('SEASide')
        self.resize(1000, 560)
        # Connection
        self._config = Configuration()
        server_names = tuple(sorted(SERVERS.keys()))
        # Interface
        wid = QWidget(self)
        self.setCentralWidget(wid)
        layout = QHBoxLayout(self)
        dropdown = QComboBox()
        dropdown.addItems(server_names)
        dropdown.setCurrentIndex(dropdown.findText(self._config.get_default_server()))
        button = QPushButton('Connect')
        layout.addWidget(button)
        layout.addWidget(dropdown)
        wid.setLayout(layout)