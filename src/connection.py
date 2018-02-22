import paramiko
import pathlib
import os.path

_key_dir = os.path.join(os.path.expanduser('~'), '.ssh')
pathlib.Path(_key_dir).mkdir(parents=True, exist_ok=True) # make ~/.ssh folder if necessary
_priv_key_path = os.path.join(_key_dir, 'seaside_rsa')
_pub_key_path = os.path.join(_key_dir, 'seaside_rsa.pub')


def _ensure_key_exists():
    """Ensure a keypair for SEASide exists and return the text of the public key"""
    if os.path.exists(_priv_key_path) and os.path.exists(_pub_key_path):
        with open(_pub_key_path, 'r') as pub_key_file:
            return pub_key_file.read()
    # Create key-pair for SEASide
    key = paramiko.RSAKey.generate(bits=1024, progress_func=lambda arg: ...)
    key.write_private_key_file(_priv_key_path) # No password protection - may want to add later
    pub_key_text = '{} {} SEASide\n'.format(key.get_name(), key.get_base64())
    with open(_pub_key_path, 'w') as pub_key_file:
        pub_key_file.write(pub_key_text)
    return pub_key_text


class Connection:
    def __init__(self, server):
        self._server = server
        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()
        self._client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self._chan = None
        self._sftp = None
        self._home_dir = None

    def _build_connection(self):
        try:
            self._chan = self._client.invoke_shell()
            self._sftp = self._client.open_sftp()
            self._sftp.chdir('.')
            self._home_dir = self._sftp.getcwd()
        except paramiko.ssh_exception.SSHException as e:
            print(e)

    def _save_keys(self):
        pub_key_text = _ensure_key_exists()
        try:
            self._sftp.stat('./.ssh')
        except FileNotFoundError:
            self._sftp.mkdir('./.ssh')
        with self._sftp.file('./.ssh/authorized_keys', 'a') as authorized_keys:
            authorized_keys.write(pub_key_text)

    def attempt_connection(self, username):
        """Returns True if connection successful returns False is unable to authenticate"""
        try:
            self._client.connect(self._server, username=username, key_filename=_priv_key_path)
        except (paramiko.AuthenticationException, paramiko.ssh_exception.SSHException) as e:
            print(e)
            return False
        else:
            self._build_connection()
            return True

    def attempt_login(self, username, password):
        try:
            self._client.connect(self._server, username=username, password=password, look_for_keys=False)
        except (paramiko.AuthenticationException, paramiko.ssh_exception.SSHException) as e:
            print(e)
            return False
        else:
            self._build_connection()
            self._save_keys()
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
        while self._chan is not None and self.has_ssh_data():
            buffer += self._chan.recv(1024)
        return buffer

    def resize_term(self, rows=24, cols=80):
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
        prefix = path + '/' if path != '/' else path
        return [prefix + filename for filename in self._sftp.listdir(path)]

    def is_dir(self, path):
        try:
            self._sftp.chdir(path)
        except (IOError, paramiko.sftp.SFTPError):
            return False
        else:
            return True
        finally:
            self._sftp.chdir("/")

    def get_home_dir(self):
        return self._home_dir