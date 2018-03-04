import sys
import os
from gui.main_window import MainWindow
from PyQt5 import QtGui
from PyQt5.QtWidgets import *


# From https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
def resource_path(path):
    base_path = getattr(sys, '_MEIPASS', os.getcwd())
    return os.path.join(base_path, path)


class SEASideApp:
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._w = MainWindow()
        self._w.setWindowIcon(QtGui.QIcon(resource_path("icons/icon.ico")))

    def run(self):
        self._w.show()
        self._app.exec_()
