"""Helper functions module."""

from lib.bme280 import BME280
from machine import Pin, I2C
import ujson
import urequests


def get_env_value(key):
    with open('env.json', encoding='utf-8') as f:
        return ujson.load(f)[key]


def get_raw_response(url):
    response = urequests.get(url)
    meta = response.json()
    response.close()
    return meta


def get_salaah_meta():
    meta = get_raw_response(
        f"https://dailyprayer.abdulrcs.repl.co/api/{get_env_value('CITY_NAME')}")

    return (
        (meta['today']['Fajr'], meta['today']['Asr']),
        (meta['today']['Sunrise'], meta['today']['Maghrib']),
        (meta['today']['Dhuhr'], meta['today']['Isha\'a']))


def get_atmospheric_meta():
    # Current weather data (external atmosphere)
    weather = get_raw_response(
        f"https://api.openweathermap.org/data/2.5/weather?q={get_env_value('CITY_NAME')},"
        + f"{get_env_value('COUNTRY_CODE')}&appid={get_env_value('APP_ID')}")

    k2c = lambda kt: round(kt - 273.15, 1)
    extemp = f"{k2c(weather['main']['temp'])}c / {weather['weather'][0]['main']}"
    exfeels = f"{k2c(weather['main']['feels_like'])}c"
    expres = f"{weather['main']['pressure']}hPa"
    exhumd = f"{weather['main']['humidity']}%"

    # BME280 sensor readings (internal atmosphere)
    intemp, inpres, inhumd = BME280(i2c=I2C(0, scl=Pin(1), sda=Pin(0))).values
    intemp = f"{round(float(intemp.replace('C', '')), 1)}c"
    inpres = f"{round(float(inpres.replace('hPa', '')))}hPa"
    inhumd = f"{round(float(inhumd.replace('%', '')))}%"

    return (
        (extemp, intemp),
        (exfeels, inpres),
        (expres, inhumd),
        (exhumd, weather['clouds']['all']))
