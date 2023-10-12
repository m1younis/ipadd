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
    # Credentials loaded from `env.json` to establish network connection
    ssid = helpers.get_env_value('SSID_NAME')
    key = helpers.get_env_value('SSID_KEY')
    if ssid and key:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, key)
        if wlan.isconnected() and wlan.status() == 3:
            wlan.scan()     # Empty scan

            # Information retrieved prior to being displayed
            prayers = helpers.get_salaah_meta()
            atmosphere = helpers.get_atmospheric_meta()
            network = helpers.get_network_meta(wlan)
            update_prayers = update_rem = False

            lcd = initialise_lcd()
            # Title height determines positioning of datetime and info
            start_ypos = display.render_title(lcd)
            display.render_salaah_meta(prayers, lcd, start_ypos)
            # Initial prayers display date recorded to determine next update
            prayers_last_updated = utime.localtime()[:3]
            display.render_atmospheric_meta(atmosphere, lcd, start_ypos)
            display.render_network_meta(network, lcd, start_ypos)

            while True:
                display.render_datetime(lcd, start_ypos)
                # Prayer times updated at the start of each day
                # Atmosphere and network sections refreshed every 5 mins of each hour
                *today, _, mm, ss = utime.localtime()[:6]
                today = tuple(today)
                if prayers_last_updated != today:
                    update_prayers = True
                    prayers = helpers.get_salaah_meta()
                if not (mm % 5 or ss):
                    update_rem = True
                    atmosphere = helpers.get_atmospheric_meta()
                    network = helpers.get_network_meta(wlan)

                utime.sleep(0.1)

                if update_prayers:
                    display.render_salaah_meta(prayers, lcd, start_ypos, on_start=False)
                    helpers.logger('Prayer times update')
                    prayers_last_updated = today
                    update_prayers = False
                if update_rem:
                    display.render_atmospheric_meta(atmosphere, lcd, ypos, on_start=False)
                    display.render_network_meta(network, lcd, ypos, on_start=False)
                    helpers.logger('Atmosphere and network meta refresh')
                    update_rem = False
        else:
            helpers.logger('Network connection failed; check supplied credentials', err=True)
    else:
        helpers.logger('Network credentials not found; check `env.json`', err=True)
