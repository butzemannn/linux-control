import unittest

from client.modules.connection_wrapper import ConnectionWrapper


class TestConnectionWrapper(unittest.TestCase):
    def test_wake_host(self):
        conn_wrapper = ConnectionWrapper()
        conn_wrapper.wake_host(wait_online=True)

    def test_wait_for_ping(self):
        conn_wrapper = ConnectionWrapper()
        conn_wrapper.wait_for_ping('127.0.0.1')


if __name__ == '__main__':
    unittest.main()
