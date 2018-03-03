from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject, pyqtSlot


class LoaderObject(QObject):
    success = pyqtSignal(str)
    failure = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, parent, username, password):
        super(LoaderObject, self).__init__()
        self._parent = parent
        self._username = username
        self._password = password

    def attempt_connect(self):
        print('Connecting')
        if self._username is None:
            self.failure.emit('')
            self.finished.emit()
            return
        conn = self._parent.get_connection()
        success = conn.attempt_login(self._username, self._password) if self._password \
            else conn.attempt_connection(self._username)
        if success:
            self.success.emit(self._username)
        else:
            self.failure.emit('Login failed')
        self.finished.emit()


class Loader(QLabel):
    success = pyqtSignal(str)
    failure = pyqtSignal(str)

    def __init__(self, parent):
        self._parent = parent
        super(Loader, self).__init__('Loading...')
        self.setAlignment(Qt.AlignHCenter)
        self.thread = None
        self.loader_obj = None

    @pyqtSlot(str)
    def connect_success(self, username):
        print('Success, username:', username)
        self.success.emit(username)

    @pyqtSlot(str)
    def connect_failure(self, error):
        print('Failure')
        self.failure.emit(error)

    def connect(self, username=None, password=None):
        self.thread = QThread()
        self.loader_obj = LoaderObject(self._parent, username, password)
        self.loader_obj.moveToThread(self.thread)
        self.thread.started.connect(self.loader_obj.attempt_connect)
        self.loader_obj.finished.connect(self.thread.quit)

        self.loader_obj.success.connect(self.connect_success)
        self.loader_obj.failure.connect(self.connect_failure)
        self.thread.start()
