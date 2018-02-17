from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Login(Widget):
    def __init__(self, error_message, **kwargs):
        super(Login, self).__init__(**kwargs)
        self.subview = GridLayout(
            pos=self.center,
            size=(200, 100),
            size_hint=(None, None))
        self.subview.cols = 2
        self.subview.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.subview.add_widget(self.username)
        self.subview.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.subview.add_widget(self.password)
        self.subview.submit = Button(text='Submit')
        self.add_widget(self.subview)