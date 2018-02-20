# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.label import Label
#
#
# class Loader(FloatLayout):
#     def __init__(self):
#         super(Loader, self).__init__(size_hint=(1, 1))
#         self.add_widget(Label(
#             text='Loading...',
#             pos_hint={'center_x': 0.5, 'center_y': 0.5},
#         ))
#
#     def connect(self, username=None, password=None):
#         if not username:
#             return self.parent.connection_failed()
#         conn = self.parent.get_connection()
#         success = conn.attempt_login(username, password) if password else conn.attempt_connection(username)
#         if success:
#             self.parent.connection_successful()
#         else:
#             self.parent.connection_failed('Login failed')
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class Loader(QLabel):
    def __init__(self, parent):
        self._parent = parent
        super(Loader, self).__init__('Loading...')
        self.setAlignment(Qt.AlignHCenter)

    def connect(self, username=None, password=None):
        if username is None:
            return self._parent.connection_failed()
        conn = self._parent.get_connection()
        success = conn.attempt_login(username, password) if password else conn.attempt_connection(username)
        if success:
            self._parent.connection_successful(username)
        else:
            self._parent.connection_failed('Login failed')