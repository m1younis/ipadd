'''
Project entry point; official Raspberry Pi datasheet referenced:
https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf
'''

import json
from machine import Pin
import network
from time import sleep
import urequests


def blink():
    led = Pin('LED', Pin.OUT)
    while True:
        led.toggle()
        sleep(0.5)


def get_env_value(key):
    with open('env.json', encoding='utf-8') as f:
        return json.load(f)[key]


def get_raw_response(url):
    response = urequests.get(url)
    meta = response.json()
    response.close()
    return meta


if __name__ == '__main__':
    ssid = get_env_value('SSID_NAME')
    key = get_env_value('SSID_KEY')
    if ssid and key:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, key)
        if wlan.isconnected():
            print(get_raw_response('http://date.jsontest.com'))
    else:
        print('Network credentials not found; check `env.json`')
