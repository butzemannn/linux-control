import io
import selectors
import socket
import struct
import json
from queue import Queue


class Message(object):

    def __init__(self, selector, sock: socket.SocketIO, addr, queue: Queue):
        self.sel = selector
        self.sock = sock
        self.queue = queue
        self.addr = addr
        self._exit = False

        self._recv_buffer = b''
        self._send_buffer = b''

        self._header = None
        self._headerlen = 2

        self._request = None
        self._encoding = "utf-8"

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()

        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()
        if len(self._recv_buffer) >= self._headerlen:
            self.process_header()

        if self._header is not None:
            self.process_request()

        if self._request is not None:
            self.queue_request()

        if self._exit:
            self.close()

    def _read(self):
        try:
            # read until connection is blocked again
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            # only run if no exception catched
            if data:
                self._recv_buffer += data
            else:
                self._exit = True

    def process_header(self) -> None:
        self._header = self._recv_buffer[:self._headerlen]
        self._header = struct.unpack(">H", self._header)[0]
        self._recv_buffer = self._recv_buffer[self._headerlen:]

    def process_request(self) -> None:
        self._request = self._recv_buffer[:self._header]
        self._request = self._request.decode(self._encoding)
        self._recv_buffer = self._recv_buffer[self._header:]

    def queue_request(self):
        """Appends the self attribute request to the queue to be executed."""
        self.queue.put(self._request)
        self._exit = True
        print(f"Request read: {self._request}")

    def write(self):
        raise NotImplementedError("Server send functionality is not implemented.")

    def close(self):
        self.sel.unregister(self.sock)
        self.sock.close()
