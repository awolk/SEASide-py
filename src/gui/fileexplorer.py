from kivy.uix.filechooser import FileChooserListLayout, FileChooserIconLayout, FileChooser


class FileExplorer(FileChooser):
    def __init__(self, **kwargs):
        super(FileExplorer, self).__init__(path='.', **kwargs)
        self.add_widget(FileChooserListLayout())
