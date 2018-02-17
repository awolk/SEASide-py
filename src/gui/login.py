from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Login(GridLayout):
    def __init__(self, error_message=''):
        super(Login, self).__init__(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size=(400, 100),
            size_hint=(None, None),
            spacing=10
        )
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self._username = TextInput(multiline=False)
        self.add_widget(self._username)
        self.add_widget(Label(text='Password'))
        self._password = TextInput(password=True, multiline=False)
        self.add_widget(self._password)
        self._submit = Button(text='Submit')
        self.add_widget(self._submit)
