"""Project entry point; official Raspberry Pi datasheet referenced:
https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf
"""

import display
import helpers
from lib.ili9341 import Display
from machine import Pin, SPI
import network
import utime


def blink():
    led = Pin('LED', Pin.OUT)
    while True:
        led.toggle()
        utime.sleep(0.5)


def initialise_lcd():
    spi = SPI(
        0,
        baudrate=10000000,
        polarity=1,
        phase=1,
        bits=8,
        firstbit=SPI.MSB,
        sck=Pin(18),
        mosi=Pin(19),
        miso=Pin(16))

    return Display(
        spi,
        dc=Pin(15),
        cs=Pin(17),
        rst=Pin(14),
        width=320,
        height=240,
        rotation=90)


if __name__ == '__main__':
    ssid = helpers.get_env_value('SSID_NAME')
    key = helpers.get_env_value('SSID_KEY')
    if ssid and key:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, key)
        if wlan.isconnected() and wlan.status() == 3:
            wlan.scan()     # Empty scan

            # Information is fetched prior to being displayed
            prayers = helpers.get_salaah_meta()

            lcd = initialise_lcd()
            # Title height determines positioning of datetime and info
            start_ypos = display.render_title(lcd)
            display.render_salaah_meta(prayers, lcd, start_ypos)

            while True:
                display.render_datetime(lcd, start_ypos)
        else:
            print('Network connection error; check supplied credentials')
    else:
        print('Network credentials not found; check `env.json`')
