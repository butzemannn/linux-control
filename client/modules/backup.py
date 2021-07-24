#!/usr/bin/env python3

import os

from client.modules.connection_wrapper import ConnectionWrapper


class Backup(object):

    def __init__(self):
        self.conn_wrapper = ConnectionWrapper()

    def backup(self):
        """Run backup job on Linux with rsync."""
        with self.conn_wrapper as conn:
            conn.send_request("start_vm")

