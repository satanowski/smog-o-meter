"""
BMP280 sensor socket server
Copyright (C) 2017 Satanowski <satanowski@gmail.com>
License: GNU AGPLv3
"""

import os
import socket
import json

from BMP280 import BMP280


class BMP280SocketServer:
    """Gets request over socket and returns current air pressure and temperature."""

    SOCKET = '/tmp/bmp280_socket'

    def __init__(self, *args):
        self._init_socket()
        self.bmp = BMP280(*args)

    def _init_socket(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            os.remove(self.SOCKET)
        except OSError:
            pass
        self.sock.bind(self.SOCKET)

    def listen(self):
        """Wait for connection. Return current measurments on any request"""
        self.sock.listen(1)
        while True:
            con, _ = self.sock.accept()
            t,p = self.bmp.measure()
            con.send("{:0.2f};{:0.2f}".format(t, p).encode())
            con.close()


if __name__ == '__main__':
    try:
        bmp_srv = BMP280SocketServer()
        bmp_srv.listen()
    except KeyboardInterrupt:
        pass

