from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QAbstractItemModel


class RemoteFileSystem(QStandardItemModel):
    def __init__(self, conn, root_path):
        super(RemoteFileSystem, self).__init__()
        self._conn = conn
        self._root_path = root_path
        parent = self.invisibleRootItem()
        self._populate(root_path, parent)

    def _populate(self, path, item):
        print('Populating', path)
        for child_filename, child_is_dir in self._conn.list_dir_stats(path):
            if not child_filename.startswith('.'):
                child_item = QStandardItem(child_filename)
                if child_is_dir:
                    self._populate(path + '/' + child_filename, child_item)
                item.appendRow(child_item)

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
                return ['Name'][section]
        return QVariant()


class FileExplorer(QTreeView):
    def __init__(self, parent):
        super(FileExplorer, self).__init__()
        self._parent = parent

    def start(self, root_path='/'):
        connection = self._parent.get_connection()
        self.setModel(RemoteFileSystem(connection, root_path))
