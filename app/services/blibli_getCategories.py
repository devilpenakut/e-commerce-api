import re
import json
from .http_utils import request_with_retry, get_proxy
from .blibli_cookies import get_blibli_cookies


def getLevel1():
    url = "https://www.blibli.com/backend/common/categories"

    payload = {}
    headers = {
        "authority": "www.blibli.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        # 'cache-control': 'no-cache',
        'cookie': get_blibli_cookies() or '',
        "referer": "https://www.blibli.com/categories",
        # 'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
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


def getLevel2(level1_id):
    url = f"https://www.blibli.com/backend/common/categories/{level1_id}/children"

    payload = {}
    headers = {
        "authority": "www.blibli.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        # 'cache-control': 'no-cache',
        'cookie': get_blibli_cookies() or '',
        "referer": "https://www.blibli.com/categories",
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


# getLevel2('19774758-1e10-453e-a3fd-88580a535020')
