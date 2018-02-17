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
        # Check if connection is made previously
        if (self.client):
            stdin, stdout, stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                # Print stdout data when available
                if stdout.channel.recv_ready():
                    # Retrieve the first 1024 bytes
                    alldata = stdout.channel.recv(1024)
                    while stdout.channel.recv_ready():
                        # Retrieve the next 1024 bytes
                        alldata += stdout.channel.recv(1024)

                    # Print as string with utf8 encoding
                    print(str(alldata, "utf8"))
        else:
            print("Connection not opened.")
        pass
    def has_ssh_data(self):
        """returns True if there is buffered data returns False otherwise"""
        pass
    def recieve_ssh_data(self):
        """returns buffered recieved data"""
        pass