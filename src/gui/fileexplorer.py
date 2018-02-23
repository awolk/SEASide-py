from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QVariant


def sizeof_fmt(num, suffix='B'):
    # Format file sizes to be human readable
    # From https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


# file model implementation inspired by
# https://stackoverflow.com/questions/46778623/lazy-loading-child-items-qtreeview

class RemoteFileSystemNode(QStandardItem):
    def __init__(self, name, conn, path, is_dir):
        super(RemoteFileSystemNode, self).__init__(name)
        self._conn = conn
        self._path = path
        self._is_dir = is_dir
        self._populated = not is_dir
        if is_dir:
            self.setData(True, RemoteFileSystem.ExpandableRole)

    def populate(self):
        if self._is_dir and not self._populated:
            for child_filename, child_is_dir, child_size in self._conn.list_dir_stats(self._path):
                if not child_filename.startswith('.'):
                    child_item = RemoteFileSystemNode(child_filename,
                                                      self._conn,
                                                      self._path + '/' + child_filename,
                                                      child_is_dir)
                    size_item = QStandardItem(sizeof_fmt(child_size) if not child_is_dir else '...')
                    self.appendRow([child_item, size_item])
            self._populated = True


class RemoteFileSystem(QStandardItemModel):
    ExpandableRole = Qt.UserRole + 500

    def __init__(self, conn, root_path):
        super(RemoteFileSystem, self).__init__()
        self._conn = conn
        self._root_path = root_path
        parent_item = self.invisibleRootItem()
        self._populate(root_path, parent_item)

    def _populate(self, path, item):
        for child_filename, child_is_dir, child_size in self._conn.list_dir_stats(path):
            if not child_filename.startswith('.'):
                child_item = RemoteFileSystemNode(child_filename,
                                                  self._conn,
                                                  path + '/' + child_filename,
                                                  child_is_dir)
                size_item = QStandardItem(sizeof_fmt(child_size) if not child_is_dir else '...')
                item.appendRow([child_item, size_item])

    def hasChildren(self, parent=None, *args, **kwargs):
        if self.data(parent, RemoteFileSystem.ExpandableRole):
            return True
        return super(RemoteFileSystem, self).hasChildren(parent, *args, **kwargs)

    def columnCount(self, parent=None, *args, **kwargs):
        return 2

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
                return ['Name', 'Size'][section]
        return QVariant()


class FileExplorer(QTreeView):
    def __init__(self, parent):
        super(FileExplorer, self).__init__()
        self._parent = parent
        self.expanded.connect(self._update)

    def start(self, root_path='/'):
        connection = self._parent.get_connection()
        self.setModel(RemoteFileSystem(connection, root_path))

    def _update(self, index):
        parent = self.model().itemFromIndex(index)
        parent.populate()