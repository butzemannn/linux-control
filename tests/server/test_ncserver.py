import socket
from unittest import TestCase

from server.modules.ncserver import NcServer


class TestNcServer(TestCase):

    def test_setup(self):
        ncserver = NcServer()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.assertRaises(ConnectionRefusedError, s.connect, ("126.0.0.1", 65432))
            ncserver.setup()
            try:
                s.connect(("127.0.0.1", 65432))
                s.shutdown(socket.SHUT_RD)
            except:
                self.fail("Connection to the socket was not possible.")

        try:
            ncserver.close()
        except:
            self.fail("Server close failed.")

    def test_run(self):
        ncserver = NcServer()
        ncserver.run()
