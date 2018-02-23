from PyQt5.QtWidgets import QWidget, QSizePolicy, QSplitter
from PyQt5.QtCore import Qt
from gui.fileexplorer import FileExplorer
from gui.terminal import Terminal


class ConnectionTab(QSplitter):
    def __init__(self):
        super(ConnectionTab, self).__init__(Qt.Horizontal)

        self._file_explorer = FileExplorer(self)
        policy = self._file_explorer.sizePolicy()
        policy.setHorizontalStretch(25)
        self._file_explorer.setSizePolicy(policy)

        self._term = Terminal(self)
        policy = self._term.sizePolicy()
        policy.setHorizontalStretch(75)
        self._term.setSizePolicy(policy)

        self.addWidget(self._file_explorer)
        self.addWidget(self._term)

    def start(self):
        self._term.start()
        self._file_explorer.start(self.get_connection().get_home_dir())

    def get_connection(self):
        return self.parent().get_connection()
