from kivy.uix.filechooser import FileChooserListLayout, FileChooser, FileSystemAbstract


class FileExplorer(FileChooser):
    def start(self, root_path='/'):
        self.connection = self.parent.get_connection()
        self.file_system = FileSystemRemote(self.connection)
        self.rootpath = root_path
        self.add_widget(FileChooserListLayout())

class FileSystemRemote(FileSystemAbstract):
    def __init__(self, connection):
        super(FileSystemRemote, self).__init__()
        self.connection = connection

    def getsize(self, fn):
        return self.connection.get_size(fn)

    def is_dir(self, fn):
        return self.connection.is_dir(fn)

    def is_hidden(self, fn):
        if fn == '/':
            return False
        return fn.split('/')[-1][0] == "."

    def listdir(self, fn):
        return self.connection.list_dir(fn)
