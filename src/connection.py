import paramiko


class Connection:
    def __init__(self, server):
        self.server = server

    def attempt_connection(self, username):
        """ returns True if connection successful returns False is unable to authenticate"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        try:
            self.client.connect(self.server, username=username)
        except paramiko.AuthenticationException:
            return False
        else:
            return True

    def attempt_login(self, username, password):
        try:
            self.client.connect(self.server, username=username, password=password)
        except paramiko.AuthenticationException:
            return False
        else:
            return True

    def send_ssh_bytes(self, bytes):

        # Check if connection is made previously
        #if (self.client):
            #stdin, stdout, stderr = self.client.exec_command(command)
            #while not stdout.channel.exit_status_ready():
                # Print stdout data when available
             #   if stdout.channel.recv_ready():
                    # Retrieve the first 1024 bytes
              #      alldata = stdout.channel.recv(1024)
               #     while stdout.channel.recv_ready():
                        # Retrieve the next 1024 bytes
                #        alldata += stdout.channel.recv(1024)

                    # Print as string with utf8 encoding
                   #print(str(alldata, "utf8"))
        #else:
         #   print("Connection not opened.")
        pass

    def has_ssh_data(self):
        """returns True if there is buffered data returns False otherwise"""
        pass

    def recieve_ssh_data(self):
        """returns buffered recieved data"""
        pass