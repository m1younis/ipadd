'''
Project entry point; official Raspberry Pi datasheet referenced:
https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf
'''

import json
from machine import Pin
from time import sleep


def blink():
    led = Pin('LED', Pin.OUT)
    while True:
        led.toggle()
        sleep(0.5)


def get_env_value(key):
    with open('env.json', encoding='utf-8') as f:
        return json.load(f)[key]


if __name__ == '__main__':
    ssid = get_env_value('SSID_NAME')
    key = get_env_value('SSID_KEY')
    if ssid and key:
        blink()
    else:
        print('Network credentials not found; check `env.json`')
