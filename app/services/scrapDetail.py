from .http_utils import request_with_retry, get_proxy, getRamdomPhoneModel
import re
from ..services.cookies import get_cookies




def getDetailProduct(url):
    # data = getRamdomPhoneModel()
    # print(url)
    # Mencari pola angka menggunakan regex
    pattern = r"i\.(\d+)\.(\d+)"
    matches = re.findall(pattern, url)

    if matches:
        shop_id, item_id = matches[0]
    else:
        print("Tidak ada angka yang cocok ditemukan.")

    
    headers = {
        "Host": "mall.shopee.co.id",
        "Referer": "https://mall.shopee.co.id",
        "X-Api-Source": "rn",
        "X-Phone-Brand": "samsung",
        "X-Phone-Model": "SM-G988N",
        "Shopee_http_dns_mode": "1",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Android app Shopee appver=29311 app_type=13",
    }

    proxies = get_proxy()
    params = {
        "shop_id": shop_id,
        "item_id": item_id,
    }

    response = request_with_retry("GET", 
        "http://147.136.167.34/api/v4/pdp/get_pc",
        params=params,
        headers=headers,
        # proxies=proxies,
        # cookies=cookies,
    )
    # print(response.json())
    return response.json()  
