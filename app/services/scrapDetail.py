import requests
import random
import string
import re
import os
import json
from ..services.cookies import get_cookies

# IMPORT FORM .env
from dotenv import load_dotenv
import os

load_dotenv()


def randomChar():
    return "".join(random.choice(string.ascii_letters) for i in range(100))

def getRamdomPhoneModel():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    devices_file_path = os.path.join(script_directory, 'devices.json')
    
    with open(devices_file_path, 'r', encoding='utf-8', errors='replace') as f:
        data = json.load(f)

        
    # cari yang key "brand" nya tidak kosong dan == samsung atau Redmi
    data = [x for x in data if x['brand'] != "" and (x['brand'] == "samsung" or x['brand'] == "Redmi")]
    # ambil random
    data = random.choice(data)
    # print(data)
    return data

def randomPort():
    # random antara 10000 - 10004 ubah ke string
    return str(random.randint(10000, 10004))


def getDetailProduct(url):
    data = getRamdomPhoneModel()
    # print(url)
  # Mencari pola angka menggunakan regex
    pattern = r"i\.(\d+)\.(\d+)"
    matches = re.findall(pattern, url)

    if matches:
        shop_id, item_id = matches[0]
        print("Shop ID:", shop_id)
        print("Item ID:", item_id)
    else:
        print("Tidak ada angka yang cocok ditemukan.")

    cookie_template = {data["name"]: data["value"] for data in get_cookies()}
    cookie_string = "; ".join([f"{key}={value}" for key, value in cookie_template.items()])
    headers = {
        "Host": "shopee.co.id",
        "Referer": "https://shopee.co.id/",
        "X-Api-Source": "rn",
        "X-Shopee-Language": "id",
        "X-Phone-Brand": data['brand'],
        "X-Phone-Model": data['device'],
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
        "shop_id": shop_id,
        "item_id": item_id,
    }

    response = requests.get(
        "https://shopee.co.id/api/v4/pdp/get_pc",
        params=params,
        headers=headers,
        proxies=proxies,
        # cookies=cookies,
    )
    return response.json()
