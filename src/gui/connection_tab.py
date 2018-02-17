from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


class ConnectionTab(FloatLayout):
    def __init__(self):
        super(ConnectionTab, self).__init__()
        self.add_widget(Label(text='Connected!', pos_hint={'center_x': 0.5, 'center_y': 0.5}))
