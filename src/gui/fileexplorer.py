from PyQt5.QtWidgets import QTreeView, QAbstractItemView, QWidget, QPushButton, QVBoxLayout, QMenu, QAction, \
    QFileDialog, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QVariant, QItemSelectionModel, QItemSelection, QModelIndex, pyqtSlot, QPoint


def sizeof_fmt(num, suffix='B'):
    # Format file sizes to be human readable. Adapted from
    # https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


# file model implementation inspired by
# https://stackoverflow.com/questions/46778623/lazy-loading-child-items-qtreeview

class RemoteFileSystemNode(QStandardItem):
    def __init__(self, name, conn, path, is_dir, size):
        super(RemoteFileSystemNode, self).__init__(name)
        self._name = name
        self._conn = conn
        self._path = path
        self._is_dir = is_dir
        self._populated = not is_dir
        self._show_hidden_files = False
        self.size_item = QStandardItem(sizeof_fmt(size) if not is_dir else '')
        if is_dir:
            self.setData(True, RemoteFileSystem.ExpandableRole)

    def name(self):
        return self._name

    def path(self):
        return self._path

    def is_dir(self):
        return self._is_dir

    def populate(self):
        if self._is_dir and not self._populated:
            self.reload()
            self._populated = True

    def is_populated(self):
        return self._populated

    def reload(self, recursive=True):
        if not self._is_dir:
            return
        children = [self.child(i) for i in range(self.rowCount())]
        path_to_child = {child.path(): child for child in children}
        # check current state of directory
        for child_filename, child_is_dir, child_size in self._conn.list_dir_stats(self._path):
            if child_filename.startswith('.') and not self._show_hidden_files:
                continue
            # check if child is already created
            path = self._path + '/' + child_filename
            if path in path_to_child:
                if recursive:
                    child = path_to_child[path]
                    child.size_item.setText(sizeof_fmt(child_size) if not child_is_dir else '')
                    if child.is_populated():
                        child.reload(recursive)  # reload child if this reload is recursive
                del path_to_child[path]
            else:  # child not created
                new_child = RemoteFileSystemNode(child_filename,
                                                 self._conn,
                                                 self._path + '/' + child_filename,
                                                 child_is_dir,
                                                 child_size)
                self.appendRow([new_child, new_child.size_item])
        # remove deleted files
        for child in path_to_child.values():
            self.takeRow(child.row())


class RemoteFileSystem(QStandardItemModel):
    ExpandableRole = Qt.UserRole + 500

    def __init__(self, conn, root_path):
        super(RemoteFileSystem, self).__init__()
        self.root = RemoteFileSystemNode(root_path, conn, root_path, True, None)
        self.root.populate()
        self.appendRow(self.root)
        self.index = self.root.index()

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


class FileTreeView(QTreeView):
    def __init__(self, parent):
        super(FileTreeView, self).__init__()
        self._root_dir = '/'
        self._parent = parent
        self._conn = None
        self._model = None

    def reload(self):
        if self._model:
            self._model.root.reload()

    def dragEnterEvent(self, evt):
        if evt.mimeData().hasUrls():  # Accept local files
            evt.accept()

    def dragMoveEvent(self, evt):
        if evt.mimeData().hasUrls():  # Accept local files
            evt.accept()
            index = self.indexAt(evt.pos())
            self.selectionModel().clear()
            self.selectionModel().select(QItemSelection(index, index), QItemSelectionModel.Select)

    def dropEvent(self, evt):
        if evt.mimeData().hasUrls():  # Accept local files
            evt.accept()
            index: QModelIndex = self.indexAt(evt.pos())
            if index.isValid():
                item = self.model().itemFromIndex(index)
                if not item.is_dir():
                    item = item.parent()
            else:
                item = self.model().root

            path = item.path()

            for url in evt.mimeData().urls():
                local_filename = url.toLocalFile()

                def callback(bytes_so_far, total_bytes):
                    if bytes_so_far == total_bytes:
                        item.reload(recursive=False)

                self._conn.file_to_remote(local_filename, path, callback)

    def start(self, root_path):
        # Build file structure
        self._root_dir = root_path
        self._conn = self._parent.get_connection()
        self._model = RemoteFileSystem(self._conn, root_path)
        self.setModel(self._model)
        self.setRootIndex(self._model.index)
        # Handle expanding folders
        self.expanded.connect(self._update)
        # Handle dropping files into file explorer
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        # Handle right clicking nodes in file explorer
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._open_menu)
        # Handle column sizing
        self.setColumnWidth(0, 150)
        self.setColumnWidth(1, 90)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)

    def _update(self, index):
        parent = self.model().itemFromIndex(index)
        parent.populate()

    @pyqtSlot(QPoint)
    def _open_menu(self, position: QPoint):
        indexes = self.selectedIndexes()
        if len(indexes) != 2:
            return
        item = self._model.itemFromIndex(indexes[0])
        if item.is_dir():
            return
        menu = QMenu()
        download_action = QAction('Download {}'.format(item.name()))
        download_action.setData({
            'path': item.path(),
            'name': item.name()
        })
        menu.addAction(download_action)
        menu.triggered.connect(self._download_menu)
        menu.exec_(self.viewport().mapToGlobal(position))

    @pyqtSlot(QAction)
    def _download_menu(self, action: QAction):
        if action.text().startswith('Download '):
            remote_path, name = action.data()['path'], action.data()['name']
            local_path = QFileDialog.getSaveFileName(caption='Save File', directory=name)[0]
            if local_path:
                self._conn.file_from_remote(remote_path, local_path)


class FileExplorer(QWidget):
    def __init__(self, parent):
        super(FileExplorer, self).__init__()
        button = QPushButton('Refresh')
        button.pressed.connect(self._btn_press)
        self._tree = FileTreeView(parent)
        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self._tree)
        self.setLayout(layout)

    @pyqtSlot()
    def _btn_press(self):
        self._tree.reload()

    def start(self, root_path='/'):
        self._tree.start(root_path)
