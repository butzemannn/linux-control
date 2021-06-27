#!/usr/bin/env python3

import socket


class ListenSocket(object):
    
    def __init__(self, host: str = "127.0.0.1", port: int = 65432):
        """
        Set up port 
        """
        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def accept(self) -> tuple:
        """
        accept blocks and waits for an incoming connection. When a client connects, it returns a new socket object
        representing the connection and a tuple holding the address of the client
        :return:
        """
        return self.socket.accept()
