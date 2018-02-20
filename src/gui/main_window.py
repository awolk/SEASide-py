from PyQt5.QtWidgets import QMainWindow, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QTabWidget
from PyQt5.QtCore import pyqtSlot

from gui.master_tab import MasterTab
from server_config import SERVERS
from savedata import Configuration


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('SEASide')
        self.resize(1000, 560)
        # Connection
        self._config = Configuration()
        server_names = tuple(sorted(SERVERS.keys()))
        # Interface
        self._widg = QWidget(self)
        self.setCentralWidget(self._widg)
        # Server selection dropdown
        self._dropdown = QComboBox()
        self._dropdown.addItems(server_names)
        default_server_name = self._config.get_default_server()
        self._dropdown.setCurrentIndex(self._dropdown.findText(default_server_name))
        # Connect button
        self._button = QPushButton('Connect')
        self._button.clicked.connect(self._new_tab)
        # Tab view
        self._tab_view = QTabWidget()
        self._tab_view.setTabsClosable(True)
        self._tab_view.tabCloseRequested.connect(self._close_tab)
        # Default tab
        default_tab = MasterTab(SERVERS[self._config.get_default_server()], self._config)
        self._tab_view.addTab(default_tab, default_server_name)
        # Layout setup
        conn_layout = QHBoxLayout()
        top_layout = QVBoxLayout()
        conn_layout.addWidget(self._button)
        conn_layout.addWidget(self._dropdown)
        conn_widg = QWidget()
        conn_widg.setLayout(conn_layout)
        top_layout.addWidget(conn_widg)
        top_layout.addWidget(self._tab_view)
        self._widg.setLayout(top_layout)

    @pyqtSlot()
    def _new_tab(self):
        server_name = str(self._dropdown.currentText())
        server = SERVERS[server_name]
        self._config.set_default_server(server_name)
        tab = MasterTab(server, self._config)
        self._tab_view.addTab(tab, server_name)
        self._tab_view.setCurrentIndex(self._tab_view.count() - 1)

    @pyqtSlot(int)
    def _close_tab(self, index):
        self._tab_view.removeTab(index)

    def get_username(self):
        return self._config.get_username()
