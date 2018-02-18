from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Login(GridLayout):
    def __init__(self, error_message=''):
        super(Login, self).__init__(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size=(400, 280),
            size_hint=(None, None),
            spacing=30
        )
        self.cols = 1
        self._error_message = Label(
            text=error_message,
            size_hint=(1, 0.5))
        self.add_widget(self._error_message)
        self.subview = GridLayout(
            pos_hint=(0.5, 0.5),
            spacing=10
        )
        self.subview.cols = 2
        self.subview.add_widget(Label(text='User Name'))
        self._username = TextInput(
            multiline=False,
            write_tab=False,
            cursor_color=(0, 0, 0, 1))
        self.subview.add_widget(self._username)
        self.subview.add_widget(Label(text='Password'))
        self._password = TextInput(
            password=True,
            multiline=False,
            write_tab=False,
            cursor_color=(0, 0, 0, 1))
        self._username.focus = True
        self._username.focus_next = self._password
        self._username.focus_previous = self._password

        self._password.focus_next = self._username
        self._username.focus_previous = self._username

        self.subview.add_widget(self._password)
        self._submit = Button(
            text='Login',
            size_hint=(1, 0.5))
        self.add_widget(self.subview)
        self.add_widget(self._submit)

    def update_error(self, error_message):
        self._error_message = Label(
            text=error_message,
            size_hint=(1, 0.5))

    def _login_attempted(self, *args):
        self.parent.give_credentials(self._username.text, self._password.text)
