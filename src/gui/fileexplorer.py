from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QAbstractItemModel


class RemoteFileSystem(QAbstractItemModel):
    def __init__(self, conn, root_path):
        super(RemoteFileSystem, self).__init__()
        self._conn = conn
        self._root_path = root_path
        self._files = list(filter(lambda file: not file.split('/')[-1].startswith('.'),
                                  self._conn.list_dir(self._root_path)))

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._files)

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def data(self, index, role=None):
        file_ind = index.row()
        if role == Qt.DisplayRole:
            return self._files[file_ind].split('/')[-1]
        return QVariant()

    def index(self, row, col, parent=None, *args, **kwargs):
        return self._files[row].split('/')[-1]

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
                return ['Name', 'Size'][section]
        return QVariant()


class FileExplorer(QTreeView):
    def __init__(self, parent):
        super(FileExplorer, self).__init__()
        self._parent = parent

    def start(self, root_path='/'):
        connection = self._parent.get_connection()
        self.setModel(RemoteFileSystem(connection, root_path))
