from kivy.uix.widget import Widget


class MasterTab(Widget):
    def __init__(self, server):
        super(MasterTab, self).__init__()
        self._server = server
