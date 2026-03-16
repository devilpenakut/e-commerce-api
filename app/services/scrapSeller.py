from .http_utils import request_with_retry, get_proxy, getRamdomPhoneModel
import string
import re
import json
import os
from ..services.cookies import get_cookies




def getShopDetail(username_store):
    data = getRamdomPhoneModel()
    cookie_template = {data["name"]: data["value"] for data in get_cookies()}
    cookie_string = "; ".join(
        [f"{key}={value}" for key, value in cookie_template.items()]
    )
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
        "keyword": "safi",
        "limit": "6",
        "offset": "0",
        "page": "search_user",
        "with_search_cover": "true",
    }

    response = request_with_retry("GET", 
        "http://147.136.167.34/api/v4/search/search_user",
        params=params,
        headers=headers,
        # proxies=proxies,
    )
    # print(response.json())
    return response.json()
