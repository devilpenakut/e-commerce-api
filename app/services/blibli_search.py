import random
import string
import re
import os
import json
import urllib.parse
from .http_utils import request_with_retry
from .blibli_cookies import get_blibli_cookies


def randomPort():
    # random antara 10000 - 10004 ubah ke string
    return str(random.randint(10000, 10004))

def clean_string(input_string):
    """Fungsi untuk membersihkan string dari karakter non-alfanumerik dan mengubahnya menjadi lowercase."""
    return re.sub(r'[^a-zA-Z0-9]', '', input_string).lower()

def match_results(data, search_term):
    """Fungsi untuk mencari `search_term` di dalam data yang diberikan."""
    # Membersihkan search_term
    clean_search_term = clean_string(search_term)
    
    # Mencari di dalam anchorStore dan nonOfficialMerchant
    for key in ['anchorStore', 'nonOfficialMerchant']:
        for store in data.get(key, []):
            term = store.get('term', '')
            # Membersihkan term dan menghapus spasi tambahan
            clean_term = clean_string(term).strip()
            if clean_search_term == clean_term:
                return store  # Mengembalikan objek store jika ditemukan
    
    return None  # Mengembalikan None jika tidak ditemukan

def searchMerchant(keyword):
    encoded = urllib.parse.quote(keyword)
    url = f'https://www.blibli.com/backend/search/autocomplete?searchTermPrefix={encoded}'

    payload = {}
    headers = {
    'authority': 'www.blibli.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.blibli.com/p/',
    "sec-ch-ua-mobile": "?1",
    'cookie': get_blibli_cookies() or '',
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.111 Mobile Safari/537.36",
    }

    proxy_url = (
        "http://firhandarief;country=ID:57fee1-d01161-63d5f9-beed9f-8105b3@38.84.70.226:"
        + randomPort()
    )
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    response = request_with_retry(
        "GET", url, headers=headers, data=payload, proxies=proxies
    )
    
    search_term = keyword
    matched_store = match_results(response.json()['data'], search_term)
    store_code = matched_store['url'].split('/')[5]
    return store_code
    
    