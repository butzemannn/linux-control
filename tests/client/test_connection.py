import struct
from unittest import TestCase

from client.modules.connection import Connection


class TestConnection(TestCase):

    def test_create_request(self):
        conn = Connection("127.0.0.1", 65432)

        # first request
        req1 = conn.create_request("Test")
        assert struct.unpack(">H", req1[:2])[0] == len("Test")
        assert req1[2:].decode() == "Test"

        # second request
        req2 = conn.create_request("start_vm 102")
        assert struct.unpack(">H", req2[:2])[0] == len("start_vm 102")
        assert req2[2:].decode() == "start_vm 102"

    def test_connect_to_socket(self):
        conn = Connection("127.0.0.1", 65432)
        conn.connect_to_socket()
        conn.disconnect_from_socket()

    def test_send_request(self):
        conn = Connection("127.0.0.1", 65432)
        conn.send_request("Test")
        conn.send_request("start_vm 102")
