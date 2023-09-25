'''
Project entry point; official Raspberry Pi datasheet referenced:
https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf
'''

from machine import Pin
from time import sleep


def blink():
    led = Pin('LED', Pin.OUT)
    while True:
        led.toggle()
        sleep(0.5)


if __name__ == '__main__':
    blink()
