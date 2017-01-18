#!/usr/bin/env python3
"""
LCD44780 display I2C library
Copyright (C) 2017 Satanowski <satanowski@gmail.com>
License: GNU AGPLv3
"""

import time

import smbus2

class LCD44780:
    """Controlls LCD display over I2C bus."""

    LINES = [0x80, 0xC0, 0x94, 0xD4]
    ENABLE = 0x4
    PULSE = 0.0005
    DELAY = 0.0005
    SEND_MODE = {"CMD": 0, "DATA": 1}
    BACKLIGHT = {True: 0x08, False: 0x00}

    def __init__(self, bus=1, i2c_address=0x3f, line_length=16, line_count=2,
                 backlight=True):
        self.address = i2c_address
        self.lcd_len = line_length
        self.lines = line_count
        self.bus = smbus2.SMBus(bus)
        self.backlight = self.BACKLIGHT[backlight]
        self._initialize()

    def _write_bus(self, data):
        self.bus.write_byte_data(self.address, 0, data)

    def _togle_enable(self, bits):
        time.sleep(self.DELAY)
        self._write_bus(bits | self.ENABLE)
        time.sleep(self.PULSE)
        self._write_bus(bits & ~self.ENABLE)
        time.sleep(self.DELAY)

    def _send_byte(self, bits, mode):
        high_bits = mode | (bits & 0xF0) | self.backlight
        low_bits = mode | ((bits<<4) & 0xF0) | self.backlight
        for bits in [high_bits, low_bits]:
            self._write_bus(bits)
            self._togle_enable(bits)

    def _initialize(self):
        init_sequence = [0x33, 0x32, 0x06, 0x0C, 0x28, 0x01]
        for cmd in init_sequence:
            self._send_byte(cmd, self.SEND_MODE['CMD'])
        time.sleep(self.DELAY)

    def clear(self):
        """Clear the display."""
        self._send_byte(0x01, self.SEND_MODE['CMD'])

    def lcd_print(self, text, line_num):
        """Print given text on line of given number(counting from 0)."""
        text = text.ljust(self.lcd_len, " ")
        self._send_byte(self.LINES[line_num], self.SEND_MODE['CMD'])
        for i in range(self.lcd_len):
            self._send_byte(ord(text[i]), self.SEND_MODE['DATA'])

