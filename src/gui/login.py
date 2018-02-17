from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Login(GridLayout):
    def __init__(self, error_message=''):
        super(Login, self).__init__(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size=(400, 350),
            size_hint=(None, None),
            spacing=30
        )
        self.cols = 1
        self.add_widget(Label(text=error_message))
        self.subview = GridLayout(
            pos_hint=(0.5, 0.5),
            spacing=10
        )
        self.subview.cols = 2
        self.subview.add_widget(Label(text='User Name'))
        self._username = TextInput(multiline=False)
        self.subview.add_widget(self._username)
        self.subview.add_widget(Label(text='Password'))
        self._password = TextInput(password=True, multiline=False)
        self.subview.add_widget(self._password)
        self._submit = Button(text='Login', on_press=self._login_pressed)
        self.add_widget(self.subview)
        self.add_widget(self._submit)

    def _login_pressed(self):
        self.parent.give_credentials(self._username.text, self._password.text)
