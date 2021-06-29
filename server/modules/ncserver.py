#!/usr/bin/env python3
import selectors
import socket
import threading
from queue import Queue

from command_execute import CommandExecute
from message import Message


class NcServer(object):

    def __init__(self):
        self.commexec = CommandExecute()
        self.queue = Queue()
        self.sel = selectors.DefaultSelector()
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()
        conn.setblocking(False)
        message = Message(self.sel, conn, addr)
        self.sel.register(conn, selectors.EVENT_READ, data=message)

    def setup(self, host: str = "127.0.0.1", port: int = 65432):
        self.lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lsock.bind((host, port))
        self.lsock.listen()
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

    def run(self):
        # 1. Start ListenSocket
        # 2. Return connections
        # 3. Create thread for connection (new ConnectionSocket)
        # 4. Parse message from connection (in thread)
        # 5. Put parsed command into queue to be executed
        # 6. Execute command from queue -> run in separate class with its own Thread
        try:
            self.setup()
            # TODO: implement way to exit loop
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        message = key.data
                        try:
                            message.process_events(mask)
                        except Exception:
                            message.close()
        finally:
            self.sel.close()

