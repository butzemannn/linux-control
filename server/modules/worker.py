import os
import sys
from queue import Queue


class Worker(object):

    def __init__(self, queue: Queue, _sentinel: object):
        # TODO: add positive response for correct commands
        self.queue = queue
        self._sentinel = _sentinel

    def start_vm(self, id: str):
        os.system(f"qm start {id}")

    def shutdown_vm(self, id: str):
        os.system(f"qm shutdown {id}")

    def test(self, arg1, arg2):
        print(f"arg1: {arg1}, arg2: {arg2}")

    def process_request(self, request: str):
        if request is self._sentinel:
            sys.exit()

        request = request.split(" ")
        try:
            func = getattr(self, request[0])
        except Exception:
            raise RuntimeError(f"Command {request[0]} not found.")

        func(*request[1:])

    def run(self):
        request = self.queue.get()
        self.process_request(request)
