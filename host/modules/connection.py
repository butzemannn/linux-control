import selectors
import socket
import struct


class Connection(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def connect_to_socket(self):
        addr = (self.host, self.port)
        print("starting connection to", addr)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect_ex(addr)

    def disconnect_from_socket(self):
        self.sock.close()

    def create_request(self, request: str):
        encoding = "utf-8"
        request = request.encode(encoding)
        header = len(request)
        header = self.encode_header(header)
        return header + request

    def encode_header(self, header) -> bytes:
        """Encodes the header to be added to message"""
        return struct.pack(">H", header)

    def send_request(self, request: str):
        """
        Sending a command as str to the remote
        :param request:
        :return:
        """
        self.connect_to_socket()
        req = self.create_request(request)
        self.sock.sendall(req)
        self.disconnect_from_socket()


