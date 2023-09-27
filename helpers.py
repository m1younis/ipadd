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
