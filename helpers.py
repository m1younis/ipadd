"""Helper functions module."""

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
