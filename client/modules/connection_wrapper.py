#!/usr/bin/env python3
import os
from types import SimpleNamespace
from wakeonlan import send_magic_packet

from client.modules.io import read_services
from connection import Connection


class ConnectionWrapper(object):

    def __init__(self):
        # TODO: move to config file (or use DNS)
        self.host_mac = "18:C0:4D:92:92:25"
        self.host_ip = "192.168.178.22"
        # TODO: verify Port
        self.host_port = 65432

        self.services = SimpleNamespace(**read_services())

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
        """Shutdowns the host."""
        raise NotImplementedError("This function is currently not implemented.")

    def is_socket_available(self) -> bool:
        """Checks if socket is available for connection"""
        # TODO: implement
        raise NotImplementedError("This function is currently not implemented.")

    def connect_to_socket(self) -> Connection:
        """Connects to the host socket."""
        # TODO: implement
        raise NotImplementedError("This function is currently not implemented.")

    def disconnect_from_socket(self):
        """Disconnect from the host's socket."""
        raise NotImplementedError("This function is currently not implemented.")

    def connect(self) -> Connection:
        """Connect to host and to the socket."""
        if not self.is_host_up():
            self.wake_host(wait_online=True, timeout=60)

        if self.is_socket_available():
            return self.connect_to_socket()
        else:
            raise RuntimeError("Cannot connect to socket.")

    def disconnect(self, shutdown: bool = False):
        self.disconnect_from_socket()
        if shutdown:
            self.shutdown_host()

    def __enter__(self, shutdown: bool = False):
        self.shutdown = shutdown
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect(self.shutdown)





