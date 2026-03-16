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


def getListProductByKey(Keyword, page):
    start = (page - 1) * 40
    encodedKeyword = urllib.parse.quote(Keyword)
    url = f"https://www.blibli.com/backend/search/products?sort=0&page={page}&start={start}&searchTerm={encodedKeyword}&intent=false&merchantSearch=true&multiCategory=true&&customUrl=&channelId=web&showFacet=false&isMobileBCA=false"

    payload = {}
    headers = {
        "authority": "www.blibli.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        # 'cache-control': 'no-cache',
        # 'channelid': 'web',
        'cookie': get_blibli_cookies() or '',
        "params": "[object Object]",
        "referer": "https://www.blibli.com/cari/baju%20koko%20anak?category=FA-1000081&category=GA-1000036&category=55076&sort=0&page=3&start=80",
        "sec-ch-ua-mobile": "?1",
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
    
    return response.json()
