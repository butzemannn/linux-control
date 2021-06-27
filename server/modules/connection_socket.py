#!/usr/bin/env python3

import socket


class ConnectionSocket(object):

    def __init__(self, conn: socket.socket, addr: str):
        self.conn = conn
        self.addr = addr

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def recv(self) -> list:
        data = []
        while True:
            data_chunk = self.conn.recv(1024)
            if not data:
                break

            data.append(data_chunk)

        return data

    def parse_message(self) -> str:
        """
        Parses message bytecode to string
        :return:
        """
        pass

