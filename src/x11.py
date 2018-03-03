import threading
import os
import Xlib.support.connect as xlib_connect


class ChannelPipe(threading.Thread):
    def __init__(self, source, destination, closed_event):
        super(ChannelPipe, self).__init__()
        self._src = source
        self._dest = destination
        self._closed_event = closed_event

    def run(self):
        while not self._src.exit_status_ready():
            if self._src.recv_ready():
                data = self._src.recv(4096)
                print('Received', len(data), 'bytes from SEASnet')
                self._dest.send(data)
        self._closed_event.set()
        self._src.close()
        self._dest.close()


class SocketPipe(ChannelPipe):
    def run(self):
        while not self._closed_event.is_set():
            try:
                self._dest.send(self._src.recv(4096))
            except IOError:
                pass


class X11Handler(threading.Thread):
    def __init__(self, transport):
        super(X11Handler, self).__init__()
        self._transport = transport

    def run(self):
        while True:
            try:
                x11_channel = self._transport.accept()
                dname, protocol, host, dno, screen = xlib_connect.get_display(os.environ['DISPLAY'])
                protocol = protocol or None
                local_x11_socket = xlib_connect.get_socket(dname, protocol, host, dno)
                # local_x11_socket.setblocking(0)
                closed_event = threading.Event()
                ChannelPipe(x11_channel, local_x11_socket, closed_event).start()
                SocketPipe(local_x11_socket, x11_channel, closed_event).start()
            except OSError:
                break