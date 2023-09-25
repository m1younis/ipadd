
from machine import Pin
from time import sleep


if __name__ == '__main__':
    led = Pin('LED', Pin.OUT)
    while True:
        led.toggle()
        sleep(0.25)
