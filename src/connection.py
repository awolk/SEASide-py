import paramiko
class Connection:
    SERVER= "lnxsrv07.seas.ucla.edu"
    def init(self, username, password):
        self.username = username
        self.password = password
    def attempt_connection(self):
        """ returns True if connection successful returns False is unable to authenticate"""
        ssh = paramiko.SSHClient()
        ssh.connect(SERVER, username=self.username, password=self.password)
    def attempt_login(username, password):
        pass
    def send_ssh_bytes(bytes):
        pass
    def has_ssh_data(self):
        """returns True if there is buffered data returns False otherwise"""
        pass
    def recieve_ssh_data(self):
        """returns buffered recieved data"""
        pass