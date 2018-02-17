from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader

from src.gui.master_tab import MasterTab

SERVERS = {
    'lnxsrv': 'lnxsrv.seas.ucla.edu',
    'lnxsrv07': 'lnxsrv07.seas.ucla.edu',
    'lnxsrv09': 'lnxsrv09.seas.ucla.edu'
}


class MainWindow(FloatLayout):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Connection
        server_names = tuple(sorted(SERVERS.keys()))
        self._spinner = Spinner(
            text=server_names[0],
            values=server_names,
            size_hint=(None, None),
            size=(300, 60)
        )
        button = Button(
            text='Connect',
            size=(300, 60),
            size_hint=(None, None)
        )
        button.bind(on_press=self._new_tab)
        top_layout = BoxLayout(
            spacing=10,
            orientation='horizontal',
            pos_hint={'top': 1, 'right': 1},
            size_hint=(None, None),
            size=(610, 60)
        )
        top_layout.add_widget(button)
        top_layout.add_widget(self._spinner)
        # Tab view
        self._tab_view = TabbedPanel()
        self._tab_view.default_tab_text = self._spinner.text
        self._tab_view.default_tab_content = MasterTab(SERVERS[self._spinner.text])
        # Build window
        self.add_widget(top_layout, 1)
        self.add_widget(self._tab_view)

    def _new_tab(self, *args):
        server_name = self._spinner.text
        server = SERVERS[server_name]
        header = TabbedPanelHeader(text=server_name)
        header.content = MasterTab(server)
        self._tab_view.add_widget(header)
