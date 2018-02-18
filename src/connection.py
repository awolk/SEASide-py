import paramiko


class Connection:
    def __init__(self, server):
        self._server = server
        self._client = paramiko.SSHClient()
        self._chan = None

    def create_chan(self):
        self._chan = self._client.invoke_shell()

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
            return True

    def attempt_login(self, username, password):
        self._client.load_system_host_keys()
        self._client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        try:
            self._client.connect(self._server, username=username, password=password)
        except (paramiko.AuthenticationException, paramiko.ssh_exception.SSHException) :
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

    def receive_ssh_data(self):
        """returns buffered received data"""
        pass

    def resize_term(self, cols=80, rows=24):
        """resizes the terminal """
        try:
            self._chan.resize_pty(width=cols, height=rows)
        except paramiko.SSHException as e:
            print(e)
