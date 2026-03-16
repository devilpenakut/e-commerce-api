import re
import json
from .http_utils import request_with_retry, get_proxy
from .blibli_cookies import get_blibli_cookies


def getLisProductByCat(cat_id, page):
    # start kelipatan 40
    start = (page - 1) * 40
    url = f"https://www.blibli.com/backend/search/products?category={cat_id}&page={page}&start={start}&channelId=web&isMobileBCA=false&showFacet=false"

    payload = {}
    headers = {
        "authority": "www.blibli.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        'cookie': get_blibli_cookies() or '',
        "params": "[object Object]",
        "referer": "https://www.blibli.com/c/",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.111 Mobile Safari/537.36",
    }

    proxies = get_proxy()
    response = request_with_retry(
        "GET", url, headers=headers, data=payload, proxies=proxies
    )
    return response.json()


