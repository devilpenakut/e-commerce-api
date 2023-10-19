import requests
import random
import string
import re
import os
import json
import urllib.parse

def randomPort():
    # random antara 10000 - 10004 ubah ke string
    return str(random.randint(10000, 10004))


def getProductByShop(shopId,page):

    url = "https://gql.tokopedia.com/graphql/ShopProducts"

    payload = json.dumps([
    {
        "operationName": "ShopProducts",
        "variables": {
        "source": "shop",
        "sid": shopId,
        "page": page,
        "perPage": 80,
        "etalaseId": "etalase",
        "sort": 1,
        "user_districtId": "2274",
        "user_cityId": "176",
        "user_lat": "",
        "user_long": ""
        },
        "query": "query ShopProducts($sid: String!, $source: String, $page: Int, $perPage: Int, $keyword: String, $etalaseId: String, $sort: Int, $user_districtId: String, $user_cityId: String, $user_lat: String, $user_long: String) {\n  GetShopProduct(shopID: $sid, source: $source, filter: {page: $page, perPage: $perPage, fkeyword: $keyword, fmenu: $etalaseId, sort: $sort, user_districtId: $user_districtId, user_cityId: $user_cityId, user_lat: $user_lat, user_long: $user_long}) {\n    status\n    errors\n    links {\n      prev\n      next\n      __typename\n    }\n    data {\n      name\n      product_url\n      product_id\n      price {\n        text_idr\n        __typename\n      }\n      primary_image {\n        original\n        thumbnail\n        resize300\n        __typename\n      }\n      flags {\n        isSold\n        isPreorder\n        isWholesale\n        isWishlist\n        __typename\n      }\n      campaign {\n        discounted_percentage\n        original_price_fmt\n        start_date\n        end_date\n        __typename\n      }\n      label {\n        color_hex\n        content\n        __typename\n      }\n      label_groups {\n        position\n        title\n        type\n        url\n        __typename\n      }\n      badge {\n        title\n        image_url\n        __typename\n      }\n      stats {\n        reviewCount\n        rating\n        averageRating\n        __typename\n      }\n      category {\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    ])
    headers = {
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'X-Version': '8ab2593',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'Referer': 'https://www.tokopedia.com/erigo/product/page/3',
    'X-Source': 'tokopedia-lite',
    'X-Device': 'default_v3',
    'X-Tkpd-Lite-Service': 'zeus',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': '_abck=7053B61DF033355E32F25D33E634A7DA~-1~YAAQXWVVuLPeQ9mKAQAAKKTA6wpAdgrTuOXg+Wmt2OrK5h9LC87Y/w6uHQTmoyXQzJbPQH4oEP/sqBKOoF3OnvfK9IddSUS6+C4MagvxP8DuAwKin41qRDq+xOzbDTCFrpAOWlWiB37cYPDv3+wRirILONDxuAnpYWrm3PjvfnAmzC0LSr6dv/OXlbfDNDzES5/zrpqv6v2FgHWR2qlIMlofpRoUShBijwfngn4zb+F5KYwU7dr5/PDHEbxBGvZ+blacpJoFQBJ9fHsbZuPHr8slWPljfoIci9T9ZOe8KKwOFrfQdyfj7eYlouHQ2uf8B3PaFg9CJKteAX7h0tFoHt+z75MlyDT5dxxL/fVvM/K/BBJtlJnjqJSwScT8OSXTwr67o53EsF9RkQtxtw==~-1~-1~-1; bm_sz=64841EBE98AA286204714DB5A578BBAB~YAAQXWVVuLTeQ9mKAQAAKKTA6xUhlURCG2RSSLW6y6lllUbQLDXo95uBVPmm7K/vlbqcfeuiKpQTu4aCAvmzaGjbUg+Bfg89WccPFimJfxp8Kwajd6UDCtA5O32thPL5E3OtE+pdj5Q+61QgjUx4rvMTySDKxp6zXsEGkBRfTT3vTlxvQrFbAvJUWI/G+ZGaOapRHqFREZtc7dPcdNW9zqf0GK7lt5fNTDd31tsheo9986BtcBHJEUNShM+9q9ABRz3yrHp/lRs1YppbjNoW/8SoAsnNtZUeWCSkNB+GCsbq380cOU0=~3224899~4338225'
    }

    proxy_url = (
        "http://firhandarief;country=ID:57fee1-d01161-63d5f9-beed9f-8105b3@38.84.70.226:"
        + randomPort()
    )
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies= proxies)

    return response.json()
