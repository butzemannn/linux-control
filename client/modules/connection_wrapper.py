#!/usr/bin/env python3
import os
from types import SimpleNamespace
from wakeonlan import send_magic_packet

from client.modules.io import read_services
from connection import Connection


class ConnectionWrapper(object):
    """
    Creates a connection to the server on which commands then can be sent. Essential steps for this
    wrapper are to check for availability of the host as well as the socket.
    """

    def __init__(self):
        # TODO: move to config file (or use DNS)
        self.host_mac = "18:C0:4D:92:92:25"
        #self.host_ip = "192.168.178.22"
        # self.host_mac = "18:C0:4D:92:92:25"
        self.host_ip = "127.0.0.1"
        # TODO: verify Port
        self.host_port = 65432

        self.services = SimpleNamespace(**read_services())
        self.connection = None

    def is_host_up(self, tries: int = 1) -> bool:
        """
        Checks if host is available

        :returns: Bool if host is currently online.
        """
        response = os.system(f"ping -c {tries} {self.host_ip}")
        if response == 0:
            return True

        return False

    def wake_host(self, wait_online: bool = False, timeout: int = 60):
        """
        Wakes up the host with a WOL magic package. Optionally waits until the server is online.
        Times out if waiting longer than timeout.

        :param wait_online: Bool which defines, if the function waits until the host is online.
        :param timeout: Timeout value in seconds.

        :raises: RuntimeError if host is already online.
        :raises: ConnectionError if wait_online times out.
        """
        if self.is_host_up():
            raise RuntimeError("Host already online.")

        send_magic_packet(self.host_mac)
        if wait_online:
            response = os.system(f"ping -c 3 -w {timeout} {self.host_ip}")
            if response != 0:
                raise ConnectionError("Host ping timed out. Host unreachable.")

    def shutdown_host(self):
        """Shuts down the host."""
        raise NotImplementedError("This function is currently not implemented.")

    def is_socket_up(self) -> bool:
        """Checks if socket is available for connection"""
        # TODO: implement
        raise NotImplementedError("This function is currently not implemented.")

    def create_connection(self) -> Connection:
        """Connects to the host socket."""
        # TODO: implement
        if self.connection is not None:
            raise ConnectionError("There already is a connection.")

        self.connection = Connection(self.host_ip, self.host_port)
        return self.connection

    def remove_connection(self):
        """Disconnect from the host's socket."""
        if self.connection is None:
            raise ConnectionError("Currently no connection available to close.")

        self.connection.disconnect()

    def connect(self) -> Connection:
        """Connect to host and to the socket."""
        if not self.is_host_up():
            self.wake_host(wait_online=True, timeout=60)

        if self.is_socket_up():
            self.connection = self.create_connection()
            return self.connection
        else:
            raise ConnectionError("Cannot connect to socket.")

    def disconnect(self, shutdown: bool = False):
        self.remove_connection()
        if shutdown:
            self.shutdown_host()

    def __enter__(self, shutdown: bool = False) -> Connection:
        self.shutdown = shutdown
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect(self.shutdown)





