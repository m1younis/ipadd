"""Helper functions module."""

from lib.bme280 import BME280
from machine import Pin, I2C
from network import WLAN
from ubinascii import hexlify
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


def strf_salaah_time(raw):
    time, period = raw.split()
    hh, mm = time.split(':')
    hh = int(hh)
    if period == 'am' and hh == 12:
        hh = 0
    elif period == 'pm' and hh != 12:
        hh += 12

    return f'{hh:02d}:{mm}'


def get_salaah_meta():
    city = get_env_value('CITY_NAME')
    try:
        meta = get_raw_response(f'https://dailyprayer.abdulrcs.repl.co/api/{city}')
        return (
            (meta['today']['Fajr'], meta['today']['Asr']),
            (meta['today']['Sunrise'], meta['today']['Maghrib']),
            (meta['today']['Dhuhr'], meta['today']['Isha\'a']))
    except Exception as e:
        meta = get_raw_response(f'https://muslimsalat.com/{city}.json')['items'][0]
        meta = {
            k: v for k, v in meta.items() if k != 'date_for'
        }
        return (
            (strf_salaah_time(meta['fajr']), strf_salaah_time(meta['asr'])),
            (strf_salaah_time(meta['shurooq']), strf_salaah_time(meta['maghrib'])),
            (strf_salaah_time(meta['dhuhr']), strf_salaah_time(meta['isha'])))


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


def decode_bin_mac(raw):
    return hexlify(raw, '-').decode()


def get_network_auth(val):
    if val == 0:
        return 'Open'
    elif val == 1:
        return 'WEP'
    elif val == 2:
        return 'WPA-PSK'
    elif val == 3:
        return 'WPA2-PSK'
    # https://github.com/orgs/micropython/discussions/10931
    elif val == 4 or val == 5:
        return 'WPA/WPA2-PSK'

    return 'Unknown'


def get_network_meta(wlan):
    if wlan.isconnected() and wlan.status() == 3:
        ip, _, rouip, _ = wlan.ifconfig()
        for ap in wlan.scan():
            if ap[0].decode() == wlan.config('ssid'):
                return (
                    (ip, rouip),
                    (decode_bin_mac(wlan.config('mac')), decode_bin_mac(ap[1])),
                    (wlan.config('hostname'), get_network_auth(ap[4])),
                    ap[3])

    return ()
