#!/usr/bin/env python3
import selectors
import socket
import threading
from queue import Queue

from worker import Worker
from message import Message


class NcServer(object):

    def __init__(self):
        self.queue = Queue()
        self.sel = selectors.DefaultSelector()
        self._sentinel = object()

        self.worker = Worker(self.queue, self._sentinel)
        self.thread = threading.Thread(target=self.worker.run)
        self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()
        conn.setblocking(False)
        message = Message(self.sel, conn, addr)
        self.sel.register(conn, selectors.EVENT_READ, data=message)

    def setup(self, host: str = "127.0.0.1", port: int = 65432):
        # setup for worker
        self.thread.start()

        # setup for listen socket
        self.lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lsock.bind((host, port))
        self.lsock.listen()
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

    def run(self):
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
            self.close()

    def close(self):
        self.sel.close()
        self.lsock.close()

        # tell thread to end and wait for it to end
        self.queue.put(self._sentinel)
        self.thread.join()
