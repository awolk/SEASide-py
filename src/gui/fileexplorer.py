from kivy.uix.widget import Widget
from kivy.uix.filechooser import FileChooserListLayout, FileChooserIconLayout, FileChooser, FileSystemAbstract


class FileExplorer(Widget):
    def start(self):
        self.connection = self.parent.get_connection()
        self.file_system = FileSystemRemote(self.connection)
        self.add_widget(FileChooser(file_system=self.file_system))


class FileSystemRemote(FileSystemAbstract):
    def __init__(self, connection):
        super(FileSystemRemote, self).__init__()
        self.connection = connection

    def get_size(self, fn):
        print("size")
        return self.connection.get_size(fn)

    def is_dir(self, fn):
        print("isdir" + fn)
        print(self.connection.is_dir(fn))
        return self.connection.is_dir(fn)

    def is_hidden(self, fn):
        print("hidden")
        return False

    def listdir(self, fn):
        print("listdir" + fn)
        print(self.connection.list_dir(fn))
        return self.connection.list_dir(fn)

