"""
BMP280 sensor I2C library
Copyright (C) 2017 Satanowski <satanowski@gmail.com>
License: GNU AGPLv3
"""

import time

import smbus2


class BMP280:
    # BMP280 Registers
    BMP280_CONTROL = 0xF4
    BMP280_CONFIG  = 0xF5
    BMP280_PRESSURE = 0xF7 # MSB, LSB, XLSB
    BMP280_TEMP = 0xFA # MSB, LSB, XLSB

    BMP280_DIG_T = [0x88, 0x8A, 0x8C]
    BMP280_DIG_P = [0x8E, 0x90, 0x92, 0x94, 0x96, 0x98, 0x9A, 0x9C, 0x9E]

    BMP280_OVRSMPL_MODE_1 = 0x27
    BMP280_STDBY_TIME_1 = 0xA0

    
    def __init__(self, bus=1, i2c_address=0x77):
        self.address = i2c_address
        self.bus = smbus2.SMBus(bus)            
        self.DIG_T = []
        self.DIG_P = []
        self._initialize()

    def _read(self, register, length=2):
        return self.bus.read_i2c_block_data(self.address, register, length)

    def _write(self, register, value):
        return self.bus.write_byte_data(self.address, register, value)

    def _read_trimming_data(self, DIG):
        lsb, msb = self._read(DIG)
        return (msb<<8) + lsb

    def _trim(self, x):
        return x-65536 if x > 32767 else x

    def _get_calibration_data(self):
        self.DIG_T = list(map(self._read_trimming_data, self.BMP280_DIG_T))
        self.DIG_T[1:] = list(map(self._trim, self.DIG_T[1:])) # trim T2 and T3

        self.DIG_P = list(map(self._read_trimming_data, self.BMP280_DIG_P))
        self.DIG_P[1:] = list(map(self._trim, self.DIG_P[1:])) # trim

    def _initialize(self):
        self._get_calibration_data()
        self._write(self.BMP280_CONTROL, self.BMP280_OVRSMPL_MODE_1)
        self._write(self.BMP280_CONFIG, self.BMP280_STDBY_TIME_1)
        time.sleep(0.5)

    def _read_adc(self, reg):
        msb, lsb, xlsb = self._read(reg, 3)
        return ((msb << 16) + (lsb << 8) + (xlsb & 0xF))/16

    def measure(self):
        adc_p, adc_t = list(map(self._read_adc, (self.BMP280_PRESSURE,self.BMP280_TEMP)))
        t1,t2,t3 = self.DIG_T
        p1,p2,p3,p4,p5,p6,p7,p8,p9 = self.DIG_P

        #temp
        t_fine = (adc_t/16384.0-t1/1024.0) * t2 + \
                 (adc_t/131072.0-t1/8192.0) * \
                 (adc_t/131072.0-t1/8192.0) * t3

        # Pressure offset calculations
        var1 = (t_fine / 2.0) - 64000.0
        var2 = ((p6 * var1**2)/32768.0 + var1*p5*2.0)/4.0 + p4*65536.0
        var1 = ((p3*var1**2)/524288.0 + p2*var1)/524288.0
        var1 = (1.0 + var1/32768.0)*p1
        p = ((1048576.0 - adc_p) - (var2/4096.0))*6250.0/var1
        var1 = (p9 * p**2)/2147483648.0
        var2 = p * p8/32768.0
        pressure = (p + (var1+var2+p7)/16.0)/100

        return (t_fine/5120.0, pressure)


if __name__ == '__main__':
    bmp = BMP280()
    t,p = bmp.mesaure()
    print("Temperature: %.2f C" % t)
    print("Pressure:    %.2f hPa" % p)

