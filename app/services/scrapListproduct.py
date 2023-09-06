import requests
import random
import string
import re
import json
import os
import http.cookies
from ..services.cookies import get_cookies

# terbaru = ctime
# terlaris = sales
# Terkaik = relevancy


def randomChar():
    return "".join(random.choice(string.ascii_letters) for i in range(100))


def getRamdomPhoneModel():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    devices_file_path = os.path.join(script_directory, "devices.json")

    with open(devices_file_path, "r", encoding="utf-8", errors="replace") as f:
        data = json.load(f)

    # cari yang key "brand" nya tidak kosong dan == samsung atau Redmi
    data = [
        x
        for x in data
        if x["brand"] != "" and (x["brand"] == "samsung" or x["brand"] == "Redmi")
    ]
    # ambil random
    data = random.choice(data)
    # print(data)
    return data


def randomPort():
    # random antara 10000 - 10004 ubah ke string
    return str(random.randint(10000, 10004))


def getListProductByKeyword(keyword, page):
    data = getRamdomPhoneModel()
    if page == 0:
        newest = "0"
    else:
        newest = (page - 1) * 60

    # cookie_template = {
    #     "SPC_R_T_ID": randomChar(),
    #     "SPC_R_T_IV": randomChar(),
    #     "SPC_T_ID": randomChar(),
    #     "SPC_T_IV": randomChar(),
    #     "REC_T_ID": randomChar(),
    #     "SPC_CLIENTID": randomChar(),
    #     "language": "id",
    #     "SPC_DID": randomChar(),
    #     "SPC_F": f"{randomChar()}_unknown",
    #     "SPC_AFTID": randomChar(),
    #     "SPC_RNBV": randomChar(),
    #     "_gcl_au": f"1.1.{randomChar()}.{randomChar()}",
    #     "_fbp": f"fb.2.{randomChar()}.{randomChar()}",
    #     "UA": f"Shopee%20Android%20Beeshop%20locale%2Fid%20version%3D738%20appver%3D29313",
    #     "SPC_SI": randomChar(),
    #     "csrftoken": randomChar(),
    # }

    # cookie_string = "; ".join(
    #     [f"{key}={value}" for key, value in cookie_template.items()]
    # )

    cookie_template = {data["name"]: data["value"] for data in get_cookies()}
    cookie_string = "; ".join([f"{key}={value}" for key, value in cookie_template.items()])
    headers = {
        "Host": "shopee.co.id",
        "Referer": "https://shopee.co.id/",
        "X-Api-Source": "rn",
        "X-Shopee-Language": "id",
        "X-Phone-Brand": data["brand"],
        "X-Phone-Model": data["device"],
        "If-None-Match-": "",
        "Shopee_http_dns_mode": "1",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Android app Shopee appver=29313 app_type=13",
        "Cookie": cookie_string,
    }
    
  

    proxy_url = (
        "http://firhandarief;country=ID:57fee1-d01161-63d5f9-beed9f-8105b3@38.84.70.226:"
        + randomPort()
    )
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    params = {
        "by": "relevancy",
        "keyword": keyword,
        "limit": "60",
        "newest": newest,
        "order": "desc",
        "page_type": "search",
        "scenario": "PAGE_GLOBAL_SEARCH",
        "version": "2",
    }

    response = requests.get(
        "https://shopee.co.id/api/v4/search/search_items",
        params=params,
        headers=headers,
        proxies=proxies,
        # cookies=cookies,
    )
    # print(response.json())
    return response.json()


def getShopDetail(username_store):
    data = getRamdomPhoneModel()
    cookie_template = {data["name"]: data["value"] for data in get_cookies()}
    cookie_string = "; ".join([f"{key}={value}" for key, value in cookie_template.items()])

    headers = {
        "Host": "shopee.co.id",
        "Referer": "https://shopee.co.id/",
        "X-Api-Source": "rn",
        "X-Shopee-Language": "id",
        "X-Phone-Brand": data["brand"],
        "X-Phone-Model": data["device"],
        "If-None-Match-": "",
        "Shopee_http_dns_mode": "1",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Android app Shopee appver=29313 app_type=13",
        "Cookie": cookie_string,
    }

    proxy_url = (
        "http://firhandarief;country=ID:57fee1-d01161-63d5f9-beed9f-8105b3@38.84.70.226:"
        + randomPort()
    )
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    params = {
        "entry_point": "",
        "need_cancel_rate": "true",
        "request_source": "shop_home_page",
        "username": "shastore08",
        "version": "1",
    }

    response = requests.get(
        "https://shopee.co.id/api/v4/shop/get_shop_base",
        params=params,
        headers=headers,
        proxies=proxies,
    )
    # print(response.json())
    return response.json()


def getLisProductByShop(shopid):
    cookie_template = {
        "SPC_R_T_ID": randomChar(),
        "SPC_R_T_IV": randomChar(),
        "SPC_T_ID": randomChar(),
        "SPC_T_IV": randomChar(),
        "REC_T_ID": randomChar(),
        "SPC_CLIENTID": randomChar(),
        "language": "id",
        "SPC_DID": randomChar(),
        "SPC_F": f"{randomChar()}_unknown",
        "SPC_AFTID": randomChar(),
        "SPC_RNBV": randomChar(),
        "_gcl_au": f"1.1.{randomChar()}.{randomChar()}",
        "_fbp": f"fb.2.{randomChar()}.{randomChar()}",
        "UA": f"Shopee%20Android%20Beeshop%20locale%2Fid%20version%3D738%20appver%3D29313",
        "SPC_SI": randomChar(),
        "csrftoken": randomChar(),
    }

    cookie_string = "; ".join(
        [f"{key}={value}" for key, value in cookie_template.items()]
    )

    referer = "https://shopee.co.id/shop/{}/search".format(shopid)
    headers = {
        "authority": "shopee.co.id",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.8",
        "referer": referer,
        "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "x-api-source": "pc",
        "x-requested-with": "XMLHttpRequest",
        "x-shopee-language": "en",
        "Cookie": cookie_string,
    }

    params = {
        "bundle": "shop_page_product_tab_main",
        "limit": "100",
        "offset": "0",
        "section": "shop_page_product_tab_main_sec",
        "shopid": shopid,
    }

    proxy_url = (
        "http://firhandarief;country=ID:57fee1-d01161-63d5f9-beed9f-8105b3@38.84.70.226:"
        + randomPort()
    )
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    response = requests.get(
        "https://shopee.co.id/api/v4/recommend/recommend",
        params=params,
        headers=headers,
        verify=False,
        proxies=proxies,
    )

    data = response.json()
    data = data["data"]
    total_product = data["sections"][0]["total"]
    print(total_product)

    # Loop through the products in batches of 100
    offset = 0
    batch_size = 100
    final_products_list = []

    while offset < total_product:
        params["offset"] = str(
            offset
        )  # Update the offset in the params for the next batch

        response = requests.get(
            "https://shopee.co.id/api/v4/recommend/recommend",
            params=params,
            headers=headers,
            verify=False,
            proxies=proxies,
        )

        data = response.json()
        products_list = data["data"]["sections"][0]["data"]["item"]
        final_products_list.extend(products_list)

        offset += batch_size

    # remove duplicate products
    final_products_list = list({v["itemid"]: v for v in final_products_list}.values())
    return final_products_list
