"""
Dust sensor I2C library
Copyright (C) 2017 Satanowski <satanowski@gmail.com>
License: GNU AGPLv3
"""

from struct import unpack_from
from collections import namedtuple

from smbus2 import SMBus

Measurement = namedtuple("Measurement", "temperature,humidity,dust")

class DrsDust:

    REGISTER=0
    
    def __init__(self, bus=1, i2c_address=0x08):
        self.address = i2c_address
        self.bus = SMBus(bus)            

    def measure(self):
        raw_data = self.bus.read_i2c_block_data(self.address, self.REGISTER, 12)
        return Measurement(*unpack_from('fff', bytes(raw_data)))


if __name__ == '__main__':
    ddust = DrsDust()
    m = ddust.measure()
    print("Temperature:  {:0.2f} \u2103".format(m.temperature))
    print("Humidity:     {:0.2f} %".format(m.humidity))
    print("Dust density: {:0.2f} ug/m\u00B3".format(m.dust))

