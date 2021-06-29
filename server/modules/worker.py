#!/usr/bin/env python3

from queue import Queue


container = {
    "overleaf": 107,
}

switcher = {
    "start": "start",
    "stop": "stop",
}


class CommandExecute(object):

    def __init__(self, queue: Queue):
        # TODO: correct queue init
        self.queue = queue

    def parse_command(self, command: str):
        try:
            func = self.switcher.get(command)

        except ValueError:
            raise ValueError(f"Parsed command {command} not found")

        return func

    def start(self):
        pass

    def stop(self):
        pass

    def start(self):
        pass

    def run(self):
        command = self.queue.get()
        func_str = self.parse_command(command)
        func = getattr(self, self.switcher[func_str])
        func()
