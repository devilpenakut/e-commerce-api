import random
import string
import re
import os
import json
import urllib.parse
from difflib import SequenceMatcher
from .http_utils import request_with_retry
from .blibli_cookies import get_blibli_cookies


def randomPort():
    # random antara 10000 - 10004 ubah ke string
    return str(random.randint(10000, 10004))


def clean_string(input_string):
    """Function to clean a string from non-alphanumeric characters and convert it to lowercase."""
    return re.sub(r"[^a-zA-Z0-9]", "", input_string).lower()


def is_similar(a, b):
    """Function to check if two strings are at least 50% similar."""
    return SequenceMatcher(None, a, b).ratio() > 0.5


def match_results(data, search_term):
    """Function to search for `search_term` within the provided data."""
    # Cleaning the search_term
    clean_search_term = clean_string(search_term)

    # Searching within anchorStore and nonOfficialMerchant
    for key in ["anchorStore", "nonOfficialMerchant"]:
        for store in data.get(key, []):
            term = store.get("term", "")
            # Cleaning term and removing additional spaces
            clean_term = clean_string(term).strip()
            if is_similar(clean_search_term, clean_term):
                return store  # Returning the store object if found

    return None  # Returning None if not found


def getMerchantCode(brandName):
    url = f"https://www.blibli.com/backend/search/brand/{brandName}?excludeProductList=true&promoTab=false&showFacet=false&multiCategory=true"

    payload = {}
    headers = {
        "authority": "www.blibli.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "referer": "https://www.blibli.com/p/",
        "cookie": get_blibli_cookies() or "",
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
    merchantCode = response.json()["data"]["products"][0]["merchantCode"]
    return merchantCode


def searchMerchant(keyword):
    encoded = urllib.parse.quote(keyword)
    url = (
        f"https://www.blibli.com/backend/search/autocomplete?searchTermPrefix={encoded}"
    )

    payload = {}
    headers = {
        "authority": "www.blibli.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "referer": "https://www.blibli.com/p/",
        "cookie": get_blibli_cookies() or "",
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

    search_term = keyword
    matched_store = match_results(response.json()["data"], search_term)
    # cek apakah matched_store['url'] mengandung /brand/ atau /merchant/
    if "/brand/" in matched_store["url"]:
        brandName = matched_store["url"].split("/")[4]
        store_code = getMerchantCode(brandName)
    else:
        store_code = matched_store["url"].split("/")[5]

    return store_code


def getInfoShop(namaToko):
    merchantCode = searchMerchant(namaToko)

    url = f"https://www.blibli.com/backend/search/merchant/{merchantCode}?excludeProductList=false&promoTab=false&pickupPointCode=null&multiCategory=true&facetOnly=true&defaultPickupPoint=true"

    payload = {}
    headers = {
        "authority": "www.blibli.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        # "cache-control": "no-cache",
        "cookie": get_blibli_cookies() or "",
        # "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEyMTkyMTciLCJhcCI6IjE1ODg4MDY1NDIiLCJpZCI6IjFiYzdjZTE1Njc3MjE4NjMiLCJ0ciI6IjNhOWZkYWZlMGJlYzVlMGVhOGM5ZjgwM2U5ODJlM2QwIiwidGkiOjE2OTg1NjA0NTQ5MzR9fQ==",
        "referer": "https://www.blibli.com/merchant/",
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

    merchant = response.json()
    merchant = merchant["data"]["merchant"]
    total_product = response.json()["data"]["paging"]['total_item']
    
    merchant["total_product"] = total_product

    return merchant
