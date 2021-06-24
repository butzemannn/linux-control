#!/usr/bin/env python3

import socket


class NasSocket(object):
    
    def __init__(self, host: str = "127.0.0.1", port: int = 65432):
        """
        Set up port 
        """
        self.host = host
        self.port = port