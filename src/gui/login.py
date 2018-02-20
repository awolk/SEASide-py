from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot


class Login(QWidget):
    def __init__(self, parent, error_message=''):
        super(Login, self).__init__()
        self._parent = parent
        # Build GUI
        form_layout = QFormLayout()
        self._username = QLineEdit()
        self._password = QLineEdit()
        self._password.setEchoMode(QLineEdit.Password)
        form_layout.addRow('Username', self._username)
        form_layout.addRow('Password', self._password)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)

        top_layout = QVBoxLayout()

        self._error_label = QLabel(error_message)
        self._error_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self._error_label)
        top_layout.addWidget(form_widget)

        login_button = QPushButton('Login')
        login_button.clicked.connect(self._attempt_login)
        self._username.returnPressed.connect(login_button.click)
        self._password.returnPressed.connect(login_button.click)

        top_layout.addWidget(login_button)
        top_layout.setAlignment(login_button, Qt.AlignHCenter)
        top_layout.addStretch()
        self.setLayout(top_layout)

    def showEvent(self, evt):
        self._username.setFocus()

    def update_error(self, error_message):
        self._error_label.setText(error_message)

    @pyqtSlot()
    def _attempt_login(self):
        self._parent.give_credentials(str(self._username.text()), str(self._password.text()))