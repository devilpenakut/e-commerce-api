import requests
import random
import string
import re
import os
import json
import urllib.parse
from difflib import SequenceMatcher


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
        "cookie": "ak_bmsc=0B1FD08A0E3F25299775AB19EA0B2C0E~000000000000000000000000000000~YAAQR5gQAmd3NGuLAQAAyq0GehW+DelWrqx5WSnQL9N95G3iYGuUF71aT0TmGLN+QPmTJn4KUeNpKmlxGv9sScgw4snUQ5jSfB5DuSsMvZ17CdAeAKHxWBllSBDhqNEdzG716YRAvENrLDckuV2mxRJlPmuIw70qdSkgM3uYnKtr4dZQ57owZudHZH7mhdsePZylBMaDd/cp1PB0yNLeNKvBUai3Zw7YHj12QdZvx1WjFu8YmafEqVQVBWQifKm75I0kkwI4BCv2md7lEi2i5RtLSKvgaVX+tdCy3eMgb6MSp4i8azRFYanAoiGgowcc5dAgunYMb3iGqFyvV0NCdEM5+ptuu1e7ES23GhiSJZ5NEGsAsoaC9csxNjzlQh8Niz7GI+sqDGqoYPzh; bm_sz=464D62CB591628AC9CAFA31CE51D065E~YAAQR5gQAml3NGuLAQAAyq0GehWa6tWPV7bhUQAkB7plEhPPfN+174tNRykKYSXUJ0qDMCsqzIP2X3KrajABtqP4s9DG39rRtbdxM0GdkTrWMNGI53WV4/QlkN6XS+vsSkPgHAiB88B8ovl+jED7C009vAiVClEW/tX7vLpzCaFyV4uZsZkbswkHX3Da5SOvUv+IUVEXtS668q2c9TgHFHuOGlwgeGQulkznK/kS7bUO7lFNmLWUbwlLIhJkl++T185staNU4Ie/m8f66LKFFHrwSechKSvYh1Xn7WYfMzyLZ5M=~3617348~4408902; Blibli-Is-Member=false; Blibli-Is-Remember=false; Blibli-Device-Id=U.5f0f2d1c-1fcb-4ca4-96fb-0a3bf801c9f3; Blibli-Device-Id-Signature=c30998000358b19d23c79431a3fd0b8d43e0189f; Blibli-User-Id=f0cdd9c5-354d-47b8-83c8-800f336d6aaf; Blibli-Session-Id=e79d6177-b91c-48de-89db-0d494196b560; Blibli-Signature=4ff8014901beaf38d68ca9aa52649ed015833c3c; Blibli-dv-id=JD_-h9VUxaOfzZlpwObqFlBW9-8QAmWgDaKbFOxV8Rk6vd; Blibli-dv-token=JT__btDmpLSYfIihBHi6ZT75KZh1M9x6pkK9kjuhzGOi7D; Blibli-dv-id-version=2; _abck=9F748555848555FC89E1DCCDC2316EED~0~YAAQR5gQApt3NGuLAQAAR7QGegpC0grMJVr3Qgx2r6yfUPcjxKbVPYYbeL3lsva26DQZpIhu94nZ58mvYLCUr6dsvvA9NnUtheas+LiMW8TS6Dfut0jGRRN7+T5AfIHMTQpleu9wQ5S17a4adWoZw8g6Dfgeip5B/DXqwoJdKV7XVrsVwO8nKQI66TkQmRxyCTW24kvAJ6zDmTfAFT55O+eQgveWJIiENrBTlskO331W8yaBNDrfUE3H8UpG43p975lLqnRZ9IoHpuzYgJwEM/APZj8UEp+o0ba/DGMfvFKLpCDpNl1gEFQQnTyqgw060tcsPPSKTKzr9Q7i3rj1EVvdP9dta24cOVOjJHT3wr+lG0tcVjPjUGnXmyCHXkGk6vFjA1OHDAwK+fH6ldmSKgQb0uW9LOTX~-1~||-1||~-1; bm_mi=F942A40E103769AC501A96A563B4F018~YAAQR5gQAnx+NGuLAQAAW4wHehVExWqr7tIn/lRjtBuVmSy+VZ+uEzsMe4oLBKcmkvy1sBm7cqsoi9Wiu92mkrYn+4lCHUqBT1fewESOmBiY+CIPCH6JdiRcUbIAgY6FhF9dhhx7O5DRNhPvqQoP8DpiSd/FLUgUVxWeLqsCir1AFFuT2f5FoSXSO6K1XPHN3m+5dJAvwmib4yBTTlWW9OOhAIF6MJvlj/q8Kt5ax+e1damhJoPRxpPRjR/K93LlG+63bOMcD57BL+JNqU36lk5/xP1Qw9RcrEV87DOWafHAHP9L0m25ktZ5br0vbJxXJS0vEImSsLY=~1; bm_sv=BC6C98A679C7A4C87C4DF2DE16A3F23B~YAAQR5gQApx+NGuLAQAATY4HehUcwh0rqKTY+ZgRJqlSEL02k3gwvb78od0XXhKfxENSSqWiTZWDvXlRYKboTd6Dc67HO2F49Ura75ZWemMdycmlx75AX59T8Ux4LIwxoB8bw3bD0lq4yT8GcydDTXzqcftZNvxzjYuF5ibFXbdBo4g+DjgeFf7phtNFd4iFf3cARYuiA7+28PANcPJhui8etxWflmalBFFo1aGfwFKxx1e3d4VcwNRlupmG9VRpdg==~1; _abck=9F748555848555FC89E1DCCDC2316EED~-1~YAAQHdxZJA2DHmyLAQAA22cSegqWHPZooNSWnkqBCU6cIamfjyF+JFUiajtleSv/m59Oicpt9Ejcn+MCtePL84wqfiMdcTU5tIcRbLF4qP22fdaYiiVDVsqilPegLferMSWo9FTZGPXnXcxD5YZJY9GE+PWRtzyZfDaqaWh81yHOLpUxGykxKK6eQwexSCwpBaWO+SYPmmvM28LqkttQZj7FSHml16iTOQy5O13tKIU+fTk0VcaRkDsWf7Oq9A58/w6MwhGkFs6S8cIwFhA3ywhxi1miMlvJqjMhnRRWW8jThvileiUCsFJqivr79IDoVYK2eQy1fW7P1v7BmScuVtCcXotM60edJOqXvKC47qDfZj7sCjhvcFH6zKaQ7J3oAOjx0SQTugUcO26jGowr6ZyzXTEaOTG7~0~-1~-1; bm_sv=BC6C98A679C7A4C87C4DF2DE16A3F23B~YAAQHdxZJA6DHmyLAQAA22cSehW8CMDhPiwfrO068eESURorwP18iDR6y4vUysVDugIT3cv2d5zcvvJEi9SDf1c+LuJ7GEFlXlsRt5ki2D9E8DDrFQwKvoQ0XZJbBj8viLbgQ/IF15zIB83f8cqhXruMdpWuOBMlTFgQTtkIhVOlvjN3qLdC9VbGUxXVlQBiZ9DDB01esoadqY+0z33LeU/a3Lt8Y9WUkA/0cb9R3YuYBKzzMCVINiA+dD8NESneNQ==~1",
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

    response = requests.request(
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
        "cookie": "ak_bmsc=0B1FD08A0E3F25299775AB19EA0B2C0E~000000000000000000000000000000~YAAQR5gQAmd3NGuLAQAAyq0GehW+DelWrqx5WSnQL9N95G3iYGuUF71aT0TmGLN+QPmTJn4KUeNpKmlxGv9sScgw4snUQ5jSfB5DuSsMvZ17CdAeAKHxWBllSBDhqNEdzG716YRAvENrLDckuV2mxRJlPmuIw70qdSkgM3uYnKtr4dZQ57owZudHZH7mhdsePZylBMaDd/cp1PB0yNLeNKvBUai3Zw7YHj12QdZvx1WjFu8YmafEqVQVBWQifKm75I0kkwI4BCv2md7lEi2i5RtLSKvgaVX+tdCy3eMgb6MSp4i8azRFYanAoiGgowcc5dAgunYMb3iGqFyvV0NCdEM5+ptuu1e7ES23GhiSJZ5NEGsAsoaC9csxNjzlQh8Niz7GI+sqDGqoYPzh; bm_sz=464D62CB591628AC9CAFA31CE51D065E~YAAQR5gQAml3NGuLAQAAyq0GehWa6tWPV7bhUQAkB7plEhPPfN+174tNRykKYSXUJ0qDMCsqzIP2X3KrajABtqP4s9DG39rRtbdxM0GdkTrWMNGI53WV4/QlkN6XS+vsSkPgHAiB88B8ovl+jED7C009vAiVClEW/tX7vLpzCaFyV4uZsZkbswkHX3Da5SOvUv+IUVEXtS668q2c9TgHFHuOGlwgeGQulkznK/kS7bUO7lFNmLWUbwlLIhJkl++T185staNU4Ie/m8f66LKFFHrwSechKSvYh1Xn7WYfMzyLZ5M=~3617348~4408902; Blibli-Is-Member=false; Blibli-Is-Remember=false; Blibli-Device-Id=U.5f0f2d1c-1fcb-4ca4-96fb-0a3bf801c9f3; Blibli-Device-Id-Signature=c30998000358b19d23c79431a3fd0b8d43e0189f; Blibli-User-Id=f0cdd9c5-354d-47b8-83c8-800f336d6aaf; Blibli-Session-Id=e79d6177-b91c-48de-89db-0d494196b560; Blibli-Signature=4ff8014901beaf38d68ca9aa52649ed015833c3c; Blibli-dv-id=JD_-h9VUxaOfzZlpwObqFlBW9-8QAmWgDaKbFOxV8Rk6vd; Blibli-dv-token=JT__btDmpLSYfIihBHi6ZT75KZh1M9x6pkK9kjuhzGOi7D; Blibli-dv-id-version=2; _abck=9F748555848555FC89E1DCCDC2316EED~0~YAAQR5gQApt3NGuLAQAAR7QGegpC0grMJVr3Qgx2r6yfUPcjxKbVPYYbeL3lsva26DQZpIhu94nZ58mvYLCUr6dsvvA9NnUtheas+LiMW8TS6Dfut0jGRRN7+T5AfIHMTQpleu9wQ5S17a4adWoZw8g6Dfgeip5B/DXqwoJdKV7XVrsVwO8nKQI66TkQmRxyCTW24kvAJ6zDmTfAFT55O+eQgveWJIiENrBTlskO331W8yaBNDrfUE3H8UpG43p975lLqnRZ9IoHpuzYgJwEM/APZj8UEp+o0ba/DGMfvFKLpCDpNl1gEFQQnTyqgw060tcsPPSKTKzr9Q7i3rj1EVvdP9dta24cOVOjJHT3wr+lG0tcVjPjUGnXmyCHXkGk6vFjA1OHDAwK+fH6ldmSKgQb0uW9LOTX~-1~||-1||~-1; bm_mi=F942A40E103769AC501A96A563B4F018~YAAQR5gQAnx+NGuLAQAAW4wHehVExWqr7tIn/lRjtBuVmSy+VZ+uEzsMe4oLBKcmkvy1sBm7cqsoi9Wiu92mkrYn+4lCHUqBT1fewESOmBiY+CIPCH6JdiRcUbIAgY6FhF9dhhx7O5DRNhPvqQoP8DpiSd/FLUgUVxWeLqsCir1AFFuT2f5FoSXSO6K1XPHN3m+5dJAvwmib4yBTTlWW9OOhAIF6MJvlj/q8Kt5ax+e1damhJoPRxpPRjR/K93LlG+63bOMcD57BL+JNqU36lk5/xP1Qw9RcrEV87DOWafHAHP9L0m25ktZ5br0vbJxXJS0vEImSsLY=~1; bm_sv=BC6C98A679C7A4C87C4DF2DE16A3F23B~YAAQR5gQApx+NGuLAQAATY4HehUcwh0rqKTY+ZgRJqlSEL02k3gwvb78od0XXhKfxENSSqWiTZWDvXlRYKboTd6Dc67HO2F49Ura75ZWemMdycmlx75AX59T8Ux4LIwxoB8bw3bD0lq4yT8GcydDTXzqcftZNvxzjYuF5ibFXbdBo4g+DjgeFf7phtNFd4iFf3cARYuiA7+28PANcPJhui8etxWflmalBFFo1aGfwFKxx1e3d4VcwNRlupmG9VRpdg==~1; _abck=9F748555848555FC89E1DCCDC2316EED~-1~YAAQHdxZJA2DHmyLAQAA22cSegqWHPZooNSWnkqBCU6cIamfjyF+JFUiajtleSv/m59Oicpt9Ejcn+MCtePL84wqfiMdcTU5tIcRbLF4qP22fdaYiiVDVsqilPegLferMSWo9FTZGPXnXcxD5YZJY9GE+PWRtzyZfDaqaWh81yHOLpUxGykxKK6eQwexSCwpBaWO+SYPmmvM28LqkttQZj7FSHml16iTOQy5O13tKIU+fTk0VcaRkDsWf7Oq9A58/w6MwhGkFs6S8cIwFhA3ywhxi1miMlvJqjMhnRRWW8jThvileiUCsFJqivr79IDoVYK2eQy1fW7P1v7BmScuVtCcXotM60edJOqXvKC47qDfZj7sCjhvcFH6zKaQ7J3oAOjx0SQTugUcO26jGowr6ZyzXTEaOTG7~0~-1~-1; bm_sv=BC6C98A679C7A4C87C4DF2DE16A3F23B~YAAQHdxZJA6DHmyLAQAA22cSehW8CMDhPiwfrO068eESURorwP18iDR6y4vUysVDugIT3cv2d5zcvvJEi9SDf1c+LuJ7GEFlXlsRt5ki2D9E8DDrFQwKvoQ0XZJbBj8viLbgQ/IF15zIB83f8cqhXruMdpWuOBMlTFgQTtkIhVOlvjN3qLdC9VbGUxXVlQBiZ9DDB01esoadqY+0z33LeU/a3Lt8Y9WUkA/0cb9R3YuYBKzzMCVINiA+dD8NESneNQ==~1",
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

    response = requests.request(
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
        "cookie": "bm_sz=464D62CB591628AC9CAFA31CE51D065E~YAAQR5gQAml3NGuLAQAAyq0GehWa6tWPV7bhUQAkB7plEhPPfN+174tNRykKYSXUJ0qDMCsqzIP2X3KrajABtqP4s9DG39rRtbdxM0GdkTrWMNGI53WV4/QlkN6XS+vsSkPgHAiB88B8ovl+jED7C009vAiVClEW/tX7vLpzCaFyV4uZsZkbswkHX3Da5SOvUv+IUVEXtS668q2c9TgHFHuOGlwgeGQulkznK/kS7bUO7lFNmLWUbwlLIhJkl++T185staNU4Ie/m8f66LKFFHrwSechKSvYh1Xn7WYfMzyLZ5M=~3617348~4408902; Blibli-Is-Member=false; Blibli-Is-Remember=false; Blibli-Device-Id=U.5f0f2d1c-1fcb-4ca4-96fb-0a3bf801c9f3; Blibli-Device-Id-Signature=c30998000358b19d23c79431a3fd0b8d43e0189f; Blibli-User-Id=f0cdd9c5-354d-47b8-83c8-800f336d6aaf; Blibli-Session-Id=e79d6177-b91c-48de-89db-0d494196b560; Blibli-Signature=4ff8014901beaf38d68ca9aa52649ed015833c3c; Blibli-dv-id=JD_-h9VUxaOfzZlpwObqFlBW9-8QAmWgDaKbFOxV8Rk6vd; Blibli-dv-token=JT__btDmpLSYfIihBHi6ZT75KZh1M9x6pkK9kjuhzGOi7D; Blibli-dv-id-version=2; _abck=9F748555848555FC89E1DCCDC2316EED~0~YAAQR5gQApt3NGuLAQAAR7QGegpC0grMJVr3Qgx2r6yfUPcjxKbVPYYbeL3lsva26DQZpIhu94nZ58mvYLCUr6dsvvA9NnUtheas+LiMW8TS6Dfut0jGRRN7+T5AfIHMTQpleu9wQ5S17a4adWoZw8g6Dfgeip5B/DXqwoJdKV7XVrsVwO8nKQI66TkQmRxyCTW24kvAJ6zDmTfAFT55O+eQgveWJIiENrBTlskO331W8yaBNDrfUE3H8UpG43p975lLqnRZ9IoHpuzYgJwEM/APZj8UEp+o0ba/DGMfvFKLpCDpNl1gEFQQnTyqgw060tcsPPSKTKzr9Q7i3rj1EVvdP9dta24cOVOjJHT3wr+lG0tcVjPjUGnXmyCHXkGk6vFjA1OHDAwK+fH6ldmSKgQb0uW9LOTX~-1~||-1||~-1; JSESSIONID=0753DE53D690C22EE8D41C9E0EC9B60A; bm_mi=F942A40E103769AC501A96A563B4F018~YAAQLiZzaGEjcmyLAQAACCMRehV1L/TnkY5qY/2O222Tc/6g9flpAe0YImmuDJMOe01KNPSq0lYMpPCDPrMWfp821pnU2MtCFqO2GEIjO50fAwcUHfNAqtX2ADYKQ84wecwwq7yY8ysyWkDgBonbWohof2Pe/lgqVhfcky+ERJnFxSOOK7zAL34pf7yWhu6x25ex7VIerd3tjq+upR+NhlvqUXJXj6JxQUiTBtD5njIf33vbxRR7WezzIMLgsQ4gQCpP18/myRypVOlVc9753MTQ/AMAt81FvVomI6cESEclA2zAULg/OSHtRwH6R6Mte8WpDjBrOL56qN8zBxIcBMswHNsSrzMRpfTf7H6EestM~1; bm_sv=BC6C98A679C7A4C87C4DF2DE16A3F23B~YAAQLiZzaHAjcmyLAQAADCcRehXHbhVyO78TPi9PeTOLoXRLfJ1QVSxRGGl8/1iZLkPaOOrJ7VMhQRKx95HHys/Y4BLAuO5zftglhmFd5uAPcLl8wq3MUvIl0cUrWv82yTWdDAU6QIhkIn7HgpZJCA/Sg3KGzy/IuzBgn2obMIPaHzBAFTseWm5GWYLqicpq70UEn1u6UMOtbyDdA3LjIpgtPxs1DHbIhbNKRO+uiRLpBzl4hlUd8Z8TJdSEdRd1nA==~1; ak_bmsc=0B1FD08A0E3F25299775AB19EA0B2C0E~000000000000000000000000000000~YAAQLiZzaIIjcmyLAQAA7pQRehWIjGoT1+SzceudSFAUGO5LPGZ77kxr7ADuAdcbBFKV98FtE/qFnLV5qFFc7dmk8ENKbUDID1UpPzVnTGdMN8TfCursDyFiRfZmThagC0suzJvGAml9zpfxBKUr1x2GAVjwBXU2iwA6Bcykne+YfXXymh7Eoqsj4asVEq8u7+bIjm2IUHiUCKlIRUQn2yUEqQkJ2QyDxViD7jvNjNNn5NQRJS6vp646vIRhiLN0CygWG+owyWq1pCNf7fQHSfuiMU0Pyplt3GhoD1+7ntaiPDs4i4hzS43qFF8drL5CInN0UuFGcQ03f6TN23c9PLp4dnV44IqNuCDzfr1L8Sh3ew91AQHySLn+AhqObjbQfgxrNUCm0lD52v857TD7ovhix+bJXrtGgv8WivWgw0Fk0+BpwqiJHLOaLeJWTJDWav6aBMuqXBSwI3r2R6CYEpK/9ic=; _abck=9F748555848555FC89E1DCCDC2316EED~-1~YAAQbvgrF6Ww92SLAQAAFt+xego9UA1VlfGuHR0U2Wy76qrDjpZ3NT13kmXXAalFBxtUKehg+zwHxb5TRlcP2dOZO7XUPQIKSaeyTVOxGHLUvw0JE0JC5BHzhWyrsTCqy0z0+hZPnI6VzaNY2YjfycMwht8sf+79PLJS1u08Ity+FLW60FX9GfMo2POo2H6N1ERnz8ljT5/rcY+cZVVhP0/COwMKKdOEEsOLHw5+TBTaiC3DWTKtfLDY8nf/9TC7fL6k67Mm9khiqP+LMTfxRhUMOO77R16bVS4OuiiF+QnJSCRUyDGml+gGWFVGFIQLooXIZVV2jwX/wfG/VgLyPG2d+5YiQ2FrC5R0NrOz/9+0yOmg5Z6QdOM4K6Hz7s544r4ebIPsEkhL7d+uZwM/Rw3mz4WSfx2K~0~-1~-1",
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

    response = requests.request(
        "GET", url, headers=headers, data=payload, proxies=proxies
    )

    merchant = response.json()
    merchant = merchant["data"]["merchant"]
    total_product = response.json()["data"]["paging"]['total_item']
    
    merchant["total_product"] = total_product

    return merchant
