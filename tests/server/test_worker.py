from unittest import TestCase

from server.modules.worker import Worker


class TestWorker(TestCase):
    def test_parse_command(self):
        self.fail()

    def test_start(self):
        self.fail()

    def test_stop(self):
        self.fail()

    def test_process_request(self):
        worker = Worker(None, object)
        worker.process_request("test 123 456")

    def test_run(self):
        self.fail()
