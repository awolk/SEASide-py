import os
import Xlib
import Xlib.support.connect as xlib_connect
import selectors


class X11Handler:
    def __init__(self, transport):
        self._transport = transport
        self._sel = selectors.DefaultSelector()
        self._sockets = []

    def _register(self, source, destination):
        try:
            self._sel.register(source, selectors.EVENT_READ, destination)
            self._sockets.append(source)
        except KeyError:
            pass

    def _unregister(self, target):
        try:
            self._sel.unregister(target)
        except (KeyError, ValueError):
            pass

    def close(self):
        for socket in self._sockets:
            socket.close()

    def step(self):
        """Step X11 handler event loop. Returns support for X11"""
        # Try to accept a new connection
        x11_channel = self._transport.accept(timeout=0)
        if x11_channel is not None:
            # Build connection
            try:
                dname, protocol, host, dno, screen = xlib_connect.get_display(os.environ['DISPLAY'])
                protocol = protocol or None
                local_x11_socket = xlib_connect.get_socket(dname, protocol, host, dno)
            except Xlib.error.DisplayConnectionError:
                return False  # X11 is not supported
            # Prevent sockets from blocking
            local_x11_socket.setblocking(False)
            x11_channel.setblocking(False)
            # Register new sockets
            self._register(x11_channel, local_x11_socket)
            self._register(local_x11_socket, x11_channel)

        # Handle communication over registered sockets
        if not self._sockets:
            return True  # Windows fails when 'selecting' nothing, so return

        events = self._sel.select(timeout=0)
        for key, mask in events:
            # send data from source to destination
            src, dest = key.fileobj, key.data
            try:
                dest.setblocking(True)
                data = src.recv(4096)
                if len(data) == 0:
                    raise OSError
                if dest.send(data) == 0:
                    raise OSError
                dest.setblocking(False)
            except OSError:
                src.close()
                dest.close()
                self._unregister(src)
                self._unregister(dest)
        # X11 is supported
        return True
