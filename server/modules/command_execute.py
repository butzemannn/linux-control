#!/usr/bin/env python3

import queue


class CommandExecute(object):

    def __init__(self):
        # TODO: correct queue init
        self.queue = queue.Queue()

    def parse_command(self):
        pass