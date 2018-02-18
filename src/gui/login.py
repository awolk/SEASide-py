from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp, sp


class Login(GridLayout):
    def __init__(self, error_message=''):
        super(Login, self).__init__(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size=(dp(300), dp(200)),
            size_hint=(None, None),
            spacing=sp(35)
        )
        self.cols = 1

        # Error Message
        self._error_message = Label(
            text=error_message,
            size_hint=(1, 0.5))
        self.add_widget(self._error_message)

        self.subview = GridLayout(
            pos_hint=(0.5, 0.5),
            spacing=sp(10)
        )
        self.subview.cols = 2
        # Username
        self.subview.add_widget(Label(text='User Name'))
        self._username = TextInput(
            multiline=False,
            write_tab=False,
            cursor_color=(0, 0, 0, 1),
            on_text_validate=self._attempt_login,

        )
        self._username.focus = True,
        self.subview.add_widget(self._username)
        # Password
        self.subview.add_widget(Label(text='Password'))
        self._password = TextInput(
            password=True,
            multiline=False,
            write_tab=False,
            cursor_color=(0, 0, 0, 1),
            on_text_validate=self._attempt_login,
        )
        self.subview.add_widget(self._password)
        self._password.focus_next = self._username
        self._password.focus_previous = self._username
        self._username.focus_next = self._password
        self._username.focus_previous = self._password
        self.add_widget(self.subview)

        # Login Button
        self._submit = Button(
            text='Login',
            size_hint=(1, 0.5),
            on_press=self._attempt_login,)
        self.add_widget(self._submit)

    def update_error(self, error_message):
        self._error_message = Label(
            text=error_message,
            size_hint=(1, 0.5))

    def _attempt_login(self, *args):
        self.parent.give_credentials(self._username.text, self._password.text)
