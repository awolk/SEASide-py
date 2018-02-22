import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from gui.main_window import MainWindow

_styles = QStyleFactory.keys()
print('Styles:', ', '.join(_styles))


class SEASideApp:
    def __init__(self):
        self._app = QApplication(sys.argv)
        # self._app.setStyle(QStyleFactory.create('Fusion'))
        self._w = MainWindow()

    def run(self):
        self._w.show()
        self._app.exec_()
