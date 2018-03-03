import sys
from gui.main_window import MainWindow
from PyQt5 import QtGui
from PyQt5.QtWidgets import *


class SEASideApp:
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._w = MainWindow()
        self._w.setWindowIcon(QtGui.QIcon("icons/icon.ico"))

    def run(self):
        self._w.show()
        self._app.exec_()
