# ipadd

A personal introduction to embedded programming and microcontrollers, the inspiration for which
stemmed from a combination of Pi-hole's [PADD](https://github.com/pi-hole/PADD) (hence the naming)
and [this](https://github.com/ak-tr/rpimon) recreation.

It serves as a real-time display centred around daily prayer times in addition to
collecting a variety of data.

![](https://github.com/m1younis/ipadd/assets/72233083/ab4feacb-fa26-45bf-84d8-08a9fb51ef6f)

> [!NOTE]
> IP and MAC addresses have been masked in the image above for demonstration purposes.

## Features

- The following information is based on your city (click [here](#configuration) to learn more):
  - Prayer times fetched from two sources; the [latter](https://muslimsalat.com/api/) is utilised
in cases where the [first](https://github.com/abdulrcs/Daily-Prayer-Time-API) is unavailable,
despite having reduced precision in comparison.
  - Weather statistics retrieved from OpenWeatherMap's extensive
[API](https://openweathermap.org/current).
- Ambient temperature, humidity and pressure readings.
- Connection configurations for your local network.

> [!NOTE]
> Local weather, internal atmosphere and network meta is refreshed once every 5 minutes of each
hour.

## Hardware

Components list:
- Raspberry Pi Pico W
- ILI9341 320x240 2.2" TFT SPI display
- BME280 sensor (Pimoroni's [version](https://shop.pimoroni.com/products/bme280-breakout) was used,
though it shouldn't matter)

The resulting circuit diagram is as follows:

![](https://github.com/m1younis/ipadd/assets/72233083/a058fb29-962e-4188-bf0b-28e8e45089da)

GPIO pins 16, 17, 18 and 19 control the LCD via SPI (default) channel 0, whilst sensor
communication is achieved over I2C (default) channel 0 by way of GPIO pins 4 and 5 as per the
Pico's
[pinout](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#pinout-and-design-files17).

### Firmware

Assuming your board hasn't been flashed yet, follow
[this](https://www.youtube.com/watch?v=GiT3MzRzG48) video tutorial to install
[Thonny](https://thonny.org) IDE along with the binary file necessary for configuring
[MicroPython](https://micropython.org).

All source code for the libraries used is found within the
[`lib`](https://github.com/m1younis/ipadd/tree/master/lib) directory - no additional dependencies
are required.

## Configuration

Ensure that `env.json` is present within the root directory of your Pico's filesystem prior to
running `main.py` as it securely stores network credentials, city and country names. Its structure
is outlined below:

```json
{
    "SSID_NAME": "router_name",
    "SSID_KEY": "router_password",
    "CITY_NAME": "your_city",
    "COUNTRY_CODE": "two_letter_country_code",
    "APP_ID": "openweathermap_api_key"
}
```

Replace each placeholder with its corresponding case-sensitive value. `APP_ID` defines an
OpenWeatherMap API key, which is generated upon registering an account
[here](https://home.openweathermap.org/users/sign_up) if you don't already have one.

## Limitations

- MicroPython's implementation of the `urequests` library is outdated and struggles to support
HTTPS requests, resulting in issues accessing a more accurate and comprehensive prayer times
[API](https://aladhan.com/prayer-times-api).
- On-board storage constraints meant functioning Python libraries (namely
[`requests`](https://pypi.org/project/requests) and
[`beautifulsoup4`](https://pypi.org/project/beautifulsoup4)) couldn't be installed locally with
their dependencies to synchronously resolve the issue above through web scraping.
- The character set for fonts provided by the display driver
[library](https://github.com/rdagger/micropython-ili9341) used were restricted, reducing visual
appeal due to the range of available symbols.
