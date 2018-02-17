from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Login(GridLayout):
    def __init__(self, error_message, **kwargs):
        super(Login, self).__init__(**kwargs)
        self.cols = 2
        if error_message is not None:
            self.add_widget(Label(text=error_message))
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
        self.submit = Button(text='Submit')


class MyApp(App):
    def build(self):
        return Login()


if __name__ == '__main__':
    MyApp().run()