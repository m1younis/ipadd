"""Project entry point; official Raspberry Pi datasheet referenced:
https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf
"""

import helpers
from machine import Pin
import network
from time import sleep


def blink():
    led = Pin('LED', Pin.OUT)
    while True:
        led.toggle()
        sleep(0.5)


if __name__ == '__main__':
    ssid = helpers.get_env_value('SSID_NAME')
    key = helpers.get_env_value('SSID_KEY')
    if ssid and key:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, key)
        if wlan.isconnected() and wlan.status() == 3:
            print(helpers.get_salaah_meta())
        else:
            print('Network connection error; check supplied credentials')
    else:
        print('Network credentials not found; check `env.json`')
