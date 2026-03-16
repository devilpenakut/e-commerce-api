from .http_utils import request_with_retry
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
    
    if page == 0:
        newest = "0"
    else:
        newest = (page - 1) * 60

   
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

    response = request_with_retry("GET", 
        "http://147.136.167.34/api/v4/search/search_items",
        params=params,
        headers=headers,
        # proxies=proxies,
        # cookies=cookies,
    )
    # print(response.json())
    return response.json()


def getShopDetail(username_store):
  

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
        "username": username_store,
        "version": "1",
    }

    response = request_with_retry("GET", 
        "http://147.136.167.34/api/v4/shop/get_shop_base",
        params=params,
        headers=headers,
        # proxies=proxies,
    )
    # print(response.json())
    return response.json()


def getLisProductByShop(shopid):
   
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

    params = {
        "bundle": "shop_page_product_tab_main",
        "limit": "100",
        "offset": "0",
        "section": "shop_page_product_tab_main_sec",
        "shop_id": shopid,
    }

    proxy_url = (
        "http://firhandarief;country=ID:57fee1-d01161-63d5f9-beed9f-8105b3@38.84.70.226:"
        + randomPort()
    )
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    response = request_with_retry("GET", 
        "http://147.136.167.34/api/v4/shop/rcmd_items",
        params=params,
        headers=headers,
        # proxies=proxies,
    )

    data = response.json()
    data = data["data"]
    total_product = data["total"]

    # Loop through the products in batches of 100
    offset = 0
    batch_size = 100
    final_products_list = []

    while offset < total_product:
        params["offset"] = str(
            offset
        )  # Update the offset in the params for the next batch

        response = request_with_retry("GET", 
            "http://147.136.167.34/api/v4/shop/rcmd_items",
            params=params,
            headers=headers,
            # proxies=proxies,
        )

        data = response.json()
        products_list = data["data"]["items"]
        final_products_list.extend(products_list)

        offset += batch_size

    # remove duplicate products
    final_products_list = list({v["itemid"]: v for v in final_products_list}.values())
    return final_products_list


def getListProductByCat(
    catid_lvl1, catid_lvl2, catid_lvl3, location, page=0, filter="pop"
):
  
    if page == 0:
        newest = "0"
    else:
        newest = (page - 1) * 60
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

    proxy_url = (
        "http://firhandarief;country=ID:57fee1-d01161-63d5f9-beed9f-8105b3@38.84.70.226:"
        + randomPort()
    )
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    params = {
        "by": filter,
        "limit": "60",
        "match_id": "",
        "newest": "0",
        "order": "desc",
        "page_type": "search",
        "scenario": "PAGE_CATEGORY",
        "version": "2",
    }

    if catid_lvl1 and not catid_lvl2 and not catid_lvl3:
        params["match_id"] = catid_lvl1
    elif catid_lvl2 and not catid_lvl1 and not catid_lvl3:
        params["match_id"] = catid_lvl2
    elif catid_lvl1 and catid_lvl3:
        params["match_id"] = catid_lvl1
        params["categoryids"] = catid_lvl3
    elif catid_lvl2 and catid_lvl3:
        params["match_id"] = catid_lvl2
        params["categoryids"] = catid_lvl3

    if location:
        # encode space to %20
        params["locations"] = re.sub(" ", "%20", location)

    # print(params)

    response = request_with_retry("GET", 
        "http://147.136.167.34/api/v4/search/search_items",
        params=params,
        headers=headers,
        # proxies=proxies,
    )
    # print(response.json())
    return response.json()
