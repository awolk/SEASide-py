from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from gui.fileexplorer import FileExplorer
from gui.terminal import Terminal


class ConnectionTab(QWidget):
    def __init__(self):
        super(ConnectionTab, self).__init__()
        self._layout = QHBoxLayout()

        self._file_explorer = FileExplorer(self)
        policy = self._file_explorer.sizePolicy()
        policy.setHorizontalStretch(25)
        self._file_explorer.setSizePolicy(policy)

        self._term = Terminal(self)
        policy = self._term.sizePolicy()
        policy.setHorizontalStretch(75)
        self._term.setSizePolicy(policy)

        self._layout.addWidget(self._file_explorer)
        self._layout.addWidget(self._term)
        self.setLayout(self._layout)

    def start(self):
        self._term.start()
        self._file_explorer.start(self.get_connection().get_home_dir())

    def get_connection(self):
        return self.parent().get_connection()
