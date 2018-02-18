from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.metrics import dp, sp
from kivy.core.window import Window

from src.gui.master_tab import MasterTab

SERVERS = {
    'lnxsrv': 'lnxsrv.seas.ucla.edu',
    'lnxsrv07': 'lnxsrv07.seas.ucla.edu',
    'lnxsrv09': 'lnxsrv09.seas.ucla.edu'
}


class MainWindow(FloatLayout):
    def __init__(self):
        super(MainWindow, self).__init__()
        Window.size = (dp(1000), dp(560))
        self._username = ''  # TODO: Get username somehow? (or don't)
        # Connection
        server_names = tuple(sorted(SERVERS.keys()))
        self._spinner = Spinner(
            text=server_names[0],
            values=server_names,
            size_hint=(None, None),
            size=(dp(80), dp(60))
        )
        button = Button(
            text='Connect',
            size=(dp(80), dp(60)),
            size_hint=(None, None)
        )
        button.bind(on_press=self._new_tab)
        top_layout = BoxLayout(
            spacing=dp(0),
            orientation='horizontal',
            pos_hint={'top': 1, 'right': 1},
            size_hint=(None, None),
            size=(dp(160), dp(55))
        )
        top_layout.add_widget(button)
        top_layout.add_widget(self._spinner)
        # Tab view
        self._tab_view = TabbedPanel()
        self._tab_view.default_tab_text = self._spinner.text
        self._tab_view.default_tab_content = MasterTab(SERVERS[self._spinner.text], self.get_username())
        # Build window
        self.add_widget(top_layout, 1)
        self.add_widget(self._tab_view)

    def _new_tab(self, *args):
        server_name = self._spinner.text
        server = SERVERS[server_name]
        header = TabbedPanelHeader(text=server_name)
        header.content = MasterTab(server, self.get_username())
        self._tab_view.add_widget(header)

    def get_username(self):
        return self._username
