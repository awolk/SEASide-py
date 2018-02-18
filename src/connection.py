import paramiko


class Connection:
    def __init__(self, server):
        self._server = server
        self._client = paramiko.SSHClient()
        self._chan = None
    def create_chan(self):
        try:
            self._chan = self._client.invoke_shell()
        except paramiko.ssh_exception.SSHException as e:
            print(e)

    def create_sftp(self):
        self._sftp = self._client.open_sftp()

    def attempt_connection(self, username):
        """ returns True if connection successful returns False is unable to authenticate"""
        self._client.load_system_host_keys()
        self._client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        try:
            self._client.connect(self._server, username=username, look_for_keys=True)
        except (paramiko.AuthenticationException, paramiko.ssh_exception.SSHException) as e:
            print(e)
            return False
        else:
            self.create_chan()
            self.create_sftp()
            return True

    def attempt_login(self, username, password):
        self._client.load_system_host_keys()
        self._client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        try:
            self._client.connect(self._server, username=username, password=password)
        except (paramiko.AuthenticationException, paramiko.ssh_exception.SSHException) as e:
            print(e)
            return False
        else:
            self.create_chan()
            self.create_sftp()
            return True

    def send_ssh_bytes(self, bytes):
        if self._chan and self._chan.send_ready():
            try:
                self._chan.send(bytes)
            except OSError:
                pass  # TODO: Implement closing connections
        else:
            print("Shell not opened")

    def has_ssh_data(self):
        """returns True if there is buffered data returns False otherwise"""
        return self._chan.recv_ready()

    def receive_ssh_data(self):
        """returns buffered received data"""
        buffer = b""
        while self._chan != None and self.has_ssh_data():
            buffer += self._chan.recv(1024)
        return buffer

    def resize_term(self, cols=80, rows=24):
        """resizes the terminal"""
        try:
            self._chan.resize_pty(width=cols, height=rows)
        except paramiko.SSHException as e:
            print(e)

    def get_size(self, filename):
        stat = self._sftp.lstat(filename)
        size = stat.st_size
        return size

    def list_dir(self, path):
        files = self._sftp.listdir(path)
        for i, file in enumerate(files):
            file = files[i]
            files[i] = path + "/" + file
        return files


    def is_dir(self, path):
        try:
            self._sftp.chdir(path)
        except (IOError, paramiko.sftp.SFTPError):
            return False
        else:
            return True
