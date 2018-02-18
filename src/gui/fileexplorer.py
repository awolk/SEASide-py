from kivy.uix.widget import Widget
from kivy.uix.filechooser import FileSystemLocal, FileChooserListLayout, FileChooser, FileSystemAbstract


class FileExplorer(FileChooser):
    def start(self):
        self.connection = self.parent.get_connection()
        self.file_system = FileSystemRemote(self.connection)
        #self.add_widget(FileChooser(file_system=self.file_system))
        self.add_widget(FileChooserListLayout())

class FileSystemRemote(FileSystemAbstract):
    def __init__(self, connection):
        super(FileSystemRemote, self).__init__()
        self.connection = connection

    def getsize(self, fn):
        print("size")
        return self.connection.get_size(fn)

    def is_dir(self, fn):
        fn = "/" + fn[1:].replace("\\", '/')
        print("isdir" + fn)
        print(self.connection.is_dir(fn))
        return self.connection.is_dir(fn)

    def is_hidden(self, fn):
        return fn[1] == "."

    def listdir(self, fn):
        fn = "/" + fn.replace("\\", '/')
        print("listdir" + fn)
        print(self.connection.list_dir(fn))
        return self.connection.list_dir(fn)
