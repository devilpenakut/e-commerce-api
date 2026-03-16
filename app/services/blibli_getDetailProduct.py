import re
import json
from .http_utils import request_with_retry, get_proxy
from .blibli_cookies import get_blibli_cookies


def getRating(productSku):

    url = f'https://www.blibli.com/backend/product-review/public-reviews?page=1&itemPerPage=5&productSku={productSku}'

    payload = {}
    headers = {
    'authority': 'www.blibli.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
     'cookie': get_blibli_cookies() or '',
    'referer': 'https://www.blibli.com/p/',
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

    return response.json()['summary']['rating']

    


def getDetailProduct(URL):
    # https://www.blibli.com/p/setelan-baju-anak-laki-laki-harian-robotic-0-8-tahun/ps--PRA-70043-00162?ds=PRA-70043-00162-00001&source=SEARCH&sid=85ee790ceaabfe94&cnc=false&pickupPointCode=PP-3189251&pid1=PRA-70043-00162&tag=trending
    match = re.search(r'\/([^\/?]+)\?.*?ds=([^&]+)', URL)
    if match:
        FormatedID = match.group(1)
        itemSku = match.group(2)
    url = f'https://www.blibli.com/backend/product-detail/products/{FormatedID}/_summary?defaultItemSku={itemSku}&pickupPointCode=null&cnc=false'

    payload = {}
    headers = {
    'authority': 'www.blibli.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
     'cookie': get_blibli_cookies() or '',
    'referer': 'https://www.blibli.com/p/',
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

    json_data = response.json()
    rating = getRating(json_data['data']['productSku'])

    newResponse = json_data
    newResponse["rating"] = rating
    return newResponse