#!/usr/bin/env python3
import sys
from queue import Queue


container = {
    "overleaf": 107,
}

commands = {
    "start": "start",
    "stop": "stop",
}


class Worker(object):

    def __init__(self, queue: Queue, _sentinel: object):
        # TODO: correct queue init
        self.queue = queue
        self._sentinel = _sentinel

        self.commands = commands
        self.container = container

    def parse_command(self, command: str):
        try:
            func = self.commands.get(command)

        except ValueError:
            raise ValueError(f"Parsed command {command} not found")

        return func

    def start(self):
        pass

    def stop(self):
        pass

    def process_request(self, request: str):
        if request is self._sentinel:
            sys.exit()

        func_str = self.parse_command(request)
        func = getattr(self, self.commands[func_str])
        func()

    def run(self):
        request = self.queue.get()
        self.process_request(request)
