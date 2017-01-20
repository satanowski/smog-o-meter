"""
LCD44780 display socket server
Copyright (C) 2017 Satanowski <satanowski@gmail.com>
License: GNU AGPLv3
"""

import os
import socket
import json

from lcd_hd_i2c import LCD44780


class LcdSocketServer:
    """Gets data over socket and prints them on LCD."""

    SOCKET = '/tmp/lcd_socket'

    def __init__(self, *args):
        self._init_socket()
        self.lcd = LCD44780(*args)
        self.lcd.clear()

    def _init_socket(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            os.remove(self.SOCKET)
        except OSError:
            pass
        self.sock.bind(self.SOCKET)

    def listen(self):
        """Read data from socket, treat them as JSON object, send it to LCD."""
        self.sock.listen(1)
        while True:
            con, adr = self.sock.accept()
            data = con.recv(1024).decode().strip()
            con.close()
            if not data:
                continue
            try:
                j = json.loads(data)
                if 'bl' in j:
                    backlight = j.pop('bl')
                else:
                    backlight = None
            except ValueError:
                continue
            for i in j:
                try:
                    line_num = int(i)
                except ValueError:
                    continue
                if backlight is not None:
                    self.lcd.set_backlight(backlight)
                self.lcd.lcd_print(j[i], line_num)


if __name__ == '__main__':
    try:
        lcd = LcdSocketServer()
        lcd.listen()
    except KeyboardInterrupt:
        pass

