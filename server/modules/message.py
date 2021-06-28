#!/usr/bin/env python3
import io
import socket
import struct
import json
from queue import Queue


class Message(object):

    def __init__(self, sock: socket.SocketIO, queue: Queue):
        self.sock = sock
        self.queue = queue

        self._recv_buffer = b''
        self._send_buffer = b''

        self._request_len = None
        self.request = None

    def _read(self):
        try:
            data = self.sock.recv(4096)

        except BlockingIOError:
            pass

        else:
            if data:
                self._recv_buffer += data

            else:
                raise RuntimeError("Peer closed connection.")

    def _process_header(self):
        headlen = 2

        if len(self._recv_buffer) >= headlen:
            self._request_len = struct.unpack(
                ">H", self._recv_buffer[:headlen]
            )[0]
            self._recv_buffer = self._recv_buffer[headlen:]

    def _process_request(self):
        encoding = "utf-8"
        if not len(self._recv_buffer) >= self._request_len:
            return

        data = self._recv_buffer[:self._request_len]
        self._recv_buffer = self._recv_buffer[self._request_len:]
        self.request = self._json_decode(data, encoding)

    def _json_decode(self, json_bytes, encoding):
        """Used if giving json dict"""
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def queue_request(self):
        """Appends the self attribute request to the queue to be executed."""
        self.queue.put(self.request)
        self.request = None

    def read(self):
        self._read()

        if self._request_len is None:
            self._process_header()

        else:
            self._process_request()
            if self.request is not None:
                self.queue_request()

    def write(self):
        raise NotImplementedError("This function is not implemented.")
