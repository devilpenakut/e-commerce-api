import time
import random
import requests


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
