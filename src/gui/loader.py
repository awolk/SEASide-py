from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


class Loader(FloatLayout):
    COUNTER = 0

    def __init__(self):
        super(Loader, self).__init__()
        self.add_widget(Label(
            text='Loading... {}'.format(Loader.COUNTER),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        ))
        Loader.COUNTER += 1

    def force_fail(self):
        self.parent.connection_failed()