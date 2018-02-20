import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


class SEASideApp:
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._w = MainWindow()

    def run(self):
        self._w.show()
        self._app.exec_()
