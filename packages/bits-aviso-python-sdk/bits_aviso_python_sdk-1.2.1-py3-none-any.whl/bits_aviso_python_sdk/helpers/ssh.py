import logging
import paramiko
import sshtunnel


class SSH:
    def __init__(self, hostname, username, password=None, key_filename=None, port=None):
        """Initializes the SSH class.

        Args:
            hostname (str): The hostname of the SSH server.
            username (str): The username to ssh_connect to the SSH server.
            password (str, optional): The password to ssh_connect to the SSH server. Defaults to None.
            key_filename (str, optional): The path to the private key file. Defaults to None.
            port (int, optional): The port to ssh_connect to the SSH server. Defaults to None.
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connected = False

    def close_connection(self):
        """Closes the SSH connection."""
        if self.connected:
            self.ssh_client.close()
            self.connected = False
            logging.info(f"Closed SSH connection to {self.hostname}.")

    def ssh_connect(self):
        """Connects to the SSH server."""
        try:
            if self.key_filename:
                self.ssh_client.connect(self.hostname, username=self.username, key_filename=self.key_filename)
            else:
                self.ssh_client.connect(self.hostname, username=self.username, password=self.password)

            self.connected = True
            logging.info(f"Connected to {self.hostname}.")

        except AttributeError as e:
            logging.error(f"Failed to ssh_connect to {self.hostname}: {e}")
            self.connected = False

    def ssh_execute_command(self, command):
        """Executes a command on the SSH server.

        Args:
            command (str): The command to execute.

        Returns:
            tuple: The standard input, standard output, and standard error of the command.
        """
        if not self.connected:
            logging.error("SSH connection not established. Ensure you have connected before executing commands.")
            return None
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return stdin, stdout.read().decode(), stderr.read().decode()

    def ssh_tunnel_forwarder(self, jumpbox_host_ip, local_bind_address="127.0.0.1", target_host_ip=None, command=None):
        if not target_host_ip:  # if target host is not provided, use the hostname
            target_host_ip = self.hostname

        logging.info(f"Starting SSH Tunnel Forwarder from {jumpbox_host_ip} to {target_host_ip}...")
        with sshtunnel.SSHTunnelForwarder(
                ssh_address_or_host=jumpbox_host_ip,
                # authenticating with the jumpbox host
                ssh_username=self.username,
                ssh_password=self.password,
                # the VPC can only touch machines on the VLAN 200
                remote_bind_address=(target_host_ip, 22),
                # binding a local host port to get session info back
                local_bind_address=(local_bind_address, 10022),
        ) as tunnel:
            logging.info(f"Successfully connected to {target_host_ip}!")
            # create ssh client
            tunnel.ssh_pkeys = []  # DIRTY HACK!
            # setting up and ssh connection on the local bind address.
            self.ssh_client.connect(local_bind_address, 10022, username=self.username, password=self.password)

            # do what needs to be done
            self.ssh_execute_command(command)

        # close_connection ssh client
        self.close_connection()
