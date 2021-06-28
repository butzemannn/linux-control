#!/usr/bin/env python3

import socket
import threading
from queue import Queue

from listen_socket import ListenSocket
from command_execute import CommandExecute


class NcServer(object):

    def __init__(self):
        self.lsocket = ListenSocket()
        self.commexec = CommandExecute
        self.queue = Queue

    def setup(self):
        pass

    def run(self):
        # 1. Start ListenSocket
        # 2. Return connections
        # 3. Create thread for connection (new ConnectionSocket)
        # 4. Parse message from connection (in thread)
        # 5. Put parsed command into queue to be executed
        # 6. Execute command from queue -> run in separate class with its own Thread
        conn, addr = self.lsocket.accept()

