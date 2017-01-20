"""
Thing speak connector
Copyright (C) 2017 Satanowski <satanowski@gmail.com>
License: GNU AGPLv3
"""

import os
import sys
import socket
from time import sleep
from datetime import datetime

import yaml
from requests import post

from DrsDust import DrsDust
from BMP280 import BMP280


class ThingSpeak:

    CFG_FILE = 'thingspeak.yaml'

    def __init__(self):
        if os.path.exists(self.CFG_FILE):
            with open(self.CFG_FILE, 'r') as f:
                self.config = yaml.load(f)
        else:
            sys.exit('No config!')

        self.bmp = BMP280()
        self.dust = DrsDust()

    def speak(self):
        bmp_m = self.bmp.measure()
        dst_m = self.dust.measure()
        fields = {
            'field1': bmp_m.temperature,
            'field2': bmp_m.pressure,
            'field3': dst_m.temperature,
            'field4': dst_m.humidity,
            'field5': dst_m.dust,
            'api_key': self.config['write_key']
        }

        return post(self.config['api_url'], fields).status_code

    def lets_talk(self):
        try:
            while True:
                r = self.speak()
                d = datetime.now().isoformat()
                if r == 200:
                    sys.stderr.write("{} Data posted\r".format(d))
                else:
                    sys.stderr.write("{} Failed to post data\r".format(d))
                sleep(60*int(self.config.get('interval', 1)))
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    ts = ThingSpeak()
    ts.lets_talk()
