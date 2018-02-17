from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button

SERVERS = {
    'lnxsrv': 'lnxsrv.seas.ucla.edu',
    'lnxsrv07': 'lnxsrv07.seas.ucla.edu',
    'lnxsrv09': 'lnxsrv09.seas.ucla.edu'
}


class MainWindow(FloatLayout):
    def __init__(self):
        super(MainWindow, self).__init__()
        server_names = tuple(sorted(SERVERS.keys()))
        spinner = Spinner(
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
        top_layout = BoxLayout(
            spacing=10,
            orientation='horizontal',
            pos_hint={'top': 1, 'right': 1},
            size_hint=(None, None),
            size=(610, 60)
        )
        top_layout.add_widget(button)
        top_layout.add_widget(spinner)
        self.add_widget(top_layout)
