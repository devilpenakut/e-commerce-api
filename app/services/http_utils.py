import time
import random
import os
import json
import requests

_DEVICES_PATH = os.path.join(os.path.dirname(__file__), "devices.json")
with open(_DEVICES_PATH, "r") as _f:
    _DEVICES = json.load(_f)


def randomPort():
    return str(random.randint(10000, 10004))


def get_proxy():
    proxy_url = (
        "http://firhandarief;country=ID:57fee1-d01161-63d5f9-beed9f-8105b3@38.84.70.226:"
        + randomPort()
    )
    return {"http": proxy_url, "https": proxy_url}


def getRamdomPhoneModel():
    filtered = [
        x for x in _DEVICES
        if x.get("brand") and (x["brand"] == "samsung" or x["brand"] == "Redmi")
    ]
    return random.choice(filtered)


def random_delay(min_sec=0.5, max_sec=2.0):
    """Jeda acak antar request untuk menghindari deteksi bot."""
    time.sleep(random.uniform(min_sec, max_sec))


def request_with_retry(method, url, max_retries=3, delay_between=2, **kwargs):
    """
    HTTP request dengan retry exponential backoff.
    Retry otomatis jika response status 403, 429, atau 503.
    """
    last_response = None
    for attempt in range(max_retries):
        random_delay()
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code in (403, 429, 503):
                wait = delay_between ** (attempt + 1)  # 2s, 4s, 8s
                time.sleep(wait)
                last_response = response
                continue
            return response
        except requests.exceptions.RequestException:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay_between ** (attempt + 1))
    return last_response
