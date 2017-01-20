"""
DustDensity sensor socket server
Copyright (C) 2017 Satanowski <satanowski@gmail.com>
License: GNU AGPLv3
"""

import os
import socket

from DrsDust import DrsDust


class DrsDustSocketServer:
    """Gets request over socket and returns current parameters of outside air
    (temp, humidity, dust density)."""

    SOCKET = '/tmp/dust_socket'

    def __init__(self, *args):
        self._init_socket()
        self.dust = DrsDust(*args)

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
            m = self.dust.measure()
            con.send("{:0.2f};{:0.2f};{:0.2f}".format(m.temperature, m.humidity, m.dust).encode())
            con.close()


if __name__ == '__main__':
    try:
        dust_srv = DrsDustSocketServer()
        dust_srv.listen()
    except KeyboardInterrupt:
        pass

