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


def pre_getListProductByShop(merchantCode, page):
    start = (page - 1) * 40
    url = f"https://www.blibli.com/backend/content/product-list?pickupPointCode=null&excludeProductList=false&promoTab=false&page={page}&start={start}&pageName=MERCHANT&pageValue={merchantCode}"

    payload = {}
    headers = {
        "authority": "www.blibli.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        # 'cookie': 'bm_sz=464D62CB591628AC9CAFA31CE51D065E~YAAQR5gQAml3NGuLAQAAyq0GehWa6tWPV7bhUQAkB7plEhPPfN+174tNRykKYSXUJ0qDMCsqzIP2X3KrajABtqP4s9DG39rRtbdxM0GdkTrWMNGI53WV4/QlkN6XS+vsSkPgHAiB88B8ovl+jED7C009vAiVClEW/tX7vLpzCaFyV4uZsZkbswkHX3Da5SOvUv+IUVEXtS668q2c9TgHFHuOGlwgeGQulkznK/kS7bUO7lFNmLWUbwlLIhJkl++T185staNU4Ie/m8f66LKFFHrwSechKSvYh1Xn7WYfMzyLZ5M=~3617348~4408902; Blibli-Is-Member=false; Blibli-Is-Remember=false; Blibli-Device-Id=U.5f0f2d1c-1fcb-4ca4-96fb-0a3bf801c9f3; Blibli-Device-Id-Signature=c30998000358b19d23c79431a3fd0b8d43e0189f; Blibli-User-Id=f0cdd9c5-354d-47b8-83c8-800f336d6aaf; Blibli-Session-Id=e79d6177-b91c-48de-89db-0d494196b560; Blibli-Signature=4ff8014901beaf38d68ca9aa52649ed015833c3c; Blibli-dv-id=JD_-h9VUxaOfzZlpwObqFlBW9-8QAmWgDaKbFOxV8Rk6vd; Blibli-dv-token=JT__btDmpLSYfIihBHi6ZT75KZh1M9x6pkK9kjuhzGOi7D; Blibli-dv-id-version=2; _abck=9F748555848555FC89E1DCCDC2316EED~0~YAAQR5gQApt3NGuLAQAAR7QGegpC0grMJVr3Qgx2r6yfUPcjxKbVPYYbeL3lsva26DQZpIhu94nZ58mvYLCUr6dsvvA9NnUtheas+LiMW8TS6Dfut0jGRRN7+T5AfIHMTQpleu9wQ5S17a4adWoZw8g6Dfgeip5B/DXqwoJdKV7XVrsVwO8nKQI66TkQmRxyCTW24kvAJ6zDmTfAFT55O+eQgveWJIiENrBTlskO331W8yaBNDrfUE3H8UpG43p975lLqnRZ9IoHpuzYgJwEM/APZj8UEp+o0ba/DGMfvFKLpCDpNl1gEFQQnTyqgw060tcsPPSKTKzr9Q7i3rj1EVvdP9dta24cOVOjJHT3wr+lG0tcVjPjUGnXmyCHXkGk6vFjA1OHDAwK+fH6ldmSKgQb0uW9LOTX~-1~||-1||~-1; JSESSIONID=0753DE53D690C22EE8D41C9E0EC9B60A; bm_mi=F942A40E103769AC501A96A563B4F018~YAAQLiZzaGEjcmyLAQAACCMRehV1L/TnkY5qY/2O222Tc/6g9flpAe0YImmuDJMOe01KNPSq0lYMpPCDPrMWfp821pnU2MtCFqO2GEIjO50fAwcUHfNAqtX2ADYKQ84wecwwq7yY8ysyWkDgBonbWohof2Pe/lgqVhfcky+ERJnFxSOOK7zAL34pf7yWhu6x25ex7VIerd3tjq+upR+NhlvqUXJXj6JxQUiTBtD5njIf33vbxRR7WezzIMLgsQ4gQCpP18/myRypVOlVc9753MTQ/AMAt81FvVomI6cESEclA2zAULg/OSHtRwH6R6Mte8WpDjBrOL56qN8zBxIcBMswHNsSrzMRpfTf7H6EestM~1; bm_sv=BC6C98A679C7A4C87C4DF2DE16A3F23B~YAAQLiZzaHAjcmyLAQAADCcRehXHbhVyO78TPi9PeTOLoXRLfJ1QVSxRGGl8/1iZLkPaOOrJ7VMhQRKx95HHys/Y4BLAuO5zftglhmFd5uAPcLl8wq3MUvIl0cUrWv82yTWdDAU6QIhkIn7HgpZJCA/Sg3KGzy/IuzBgn2obMIPaHzBAFTseWm5GWYLqicpq70UEn1u6UMOtbyDdA3LjIpgtPxs1DHbIhbNKRO+uiRLpBzl4hlUd8Z8TJdSEdRd1nA==~1; ak_bmsc=0B1FD08A0E3F25299775AB19EA0B2C0E~000000000000000000000000000000~YAAQLiZzaIIjcmyLAQAA7pQRehWIjGoT1+SzceudSFAUGO5LPGZ77kxr7ADuAdcbBFKV98FtE/qFnLV5qFFc7dmk8ENKbUDID1UpPzVnTGdMN8TfCursDyFiRfZmThagC0suzJvGAml9zpfxBKUr1x2GAVjwBXU2iwA6Bcykne+YfXXymh7Eoqsj4asVEq8u7+bIjm2IUHiUCKlIRUQn2yUEqQkJ2QyDxViD7jvNjNNn5NQRJS6vp646vIRhiLN0CygWG+owyWq1pCNf7fQHSfuiMU0Pyplt3GhoD1+7ntaiPDs4i4hzS43qFF8drL5CInN0UuFGcQ03f6TN23c9PLp4dnV44IqNuCDzfr1L8Sh3ew91AQHySLn+AhqObjbQfgxrNUCm0lD52v857TD7ovhix+bJXrtGgv8WivWgw0Fk0+BpwqiJHLOaLeJWTJDWav6aBMuqXBSwI3r2R6CYEpK/9ic=; _abck=9F748555848555FC89E1DCCDC2316EED~-1~YAAQ7V9idvfut22LAQAAB8cVegqOqvvE8ldLvIR7aHYaIbLP9Mez+5HnX2wDvuy0w6ykl5I2HiFWXFHEgb/fJTaTXIDrL/Nw47weIZwujYPjb5E4fAyFeANammnJlnkTXWAiWj/s9qYRDb6CMzyPDmy5ZuxEpFt79IMZogWXPOFlPD/wjvDs122dyFakn9OtxqoWwQLNwWn3b1pjff1l4xuQb/AXnU2UpFc7tpjhEVsxRCkx//6oZ331gFPDSTg4/kvvBrorjIwA9bjcwbUDsCJ1mkyekDtPgn3QqF1/Hqp4Q2Ws9S7USomZbwhE7sQYQVOq465/a7+V8u+NJXQrn1sUzXoH8LI3vhyfwvNpgJ/lNKbsUg6DZcad8Vbh7/LbcIXY8Ke4w+16gPWNWkVg2XIwlkwCxk0+~0~-1~-1; bm_sv=BC6C98A679C7A4C87C4DF2DE16A3F23B~YAAQHdxZJA6DHmyLAQAA22cSehW8CMDhPiwfrO068eESURorwP18iDR6y4vUysVDugIT3cv2d5zcvvJEi9SDf1c+LuJ7GEFlXlsRt5ki2D9E8DDrFQwKvoQ0XZJbBj8viLbgQ/IF15zIB83f8cqhXruMdpWuOBMlTFgQTtkIhVOlvjN3qLdC9VbGUxXVlQBiZ9DDB01esoadqY+0z33LeU/a3Lt8Y9WUkA/0cb9R3YuYBKzzMCVINiA+dD8NESneNQ==~1',
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

    return True


def getListProductByShop(merchantCode, page):
    start = (page - 1) * 40
    url =f'https://www.blibli.com/backend/search/merchant/{merchantCode}?excludeProductList=false&promoTab=false&pickupPointCode=null&page={page}&start={start}&multiCategory=true&merchantSearch=false&pickupPointLatLong=&showFacet=false&defaultPickupPoint=true'

    payload = {}
    headers = {
        "authority": "www.blibli.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        # 'cache-control': 'no-cache',
        # 'channelid': 'web',
        # 'cookie': 'bm_sz=464D62CB591628AC9CAFA31CE51D065E~YAAQR5gQAml3NGuLAQAAyq0GehWa6tWPV7bhUQAkB7plEhPPfN+174tNRykKYSXUJ0qDMCsqzIP2X3KrajABtqP4s9DG39rRtbdxM0GdkTrWMNGI53WV4/QlkN6XS+vsSkPgHAiB88B8ovl+jED7C009vAiVClEW/tX7vLpzCaFyV4uZsZkbswkHX3Da5SOvUv+IUVEXtS668q2c9TgHFHuOGlwgeGQulkznK/kS7bUO7lFNmLWUbwlLIhJkl++T185staNU4Ie/m8f66LKFFHrwSechKSvYh1Xn7WYfMzyLZ5M=~3617348~4408902; Blibli-Is-Member=false; Blibli-Is-Remember=false; Blibli-Device-Id=U.5f0f2d1c-1fcb-4ca4-96fb-0a3bf801c9f3; Blibli-Device-Id-Signature=c30998000358b19d23c79431a3fd0b8d43e0189f; Blibli-User-Id=f0cdd9c5-354d-47b8-83c8-800f336d6aaf; Blibli-Session-Id=e79d6177-b91c-48de-89db-0d494196b560; Blibli-Signature=4ff8014901beaf38d68ca9aa52649ed015833c3c; Blibli-dv-id=JD_-h9VUxaOfzZlpwObqFlBW9-8QAmWgDaKbFOxV8Rk6vd; Blibli-dv-token=JT__btDmpLSYfIihBHi6ZT75KZh1M9x6pkK9kjuhzGOi7D; Blibli-dv-id-version=2; _abck=9F748555848555FC89E1DCCDC2316EED~0~YAAQR5gQApt3NGuLAQAAR7QGegpC0grMJVr3Qgx2r6yfUPcjxKbVPYYbeL3lsva26DQZpIhu94nZ58mvYLCUr6dsvvA9NnUtheas+LiMW8TS6Dfut0jGRRN7+T5AfIHMTQpleu9wQ5S17a4adWoZw8g6Dfgeip5B/DXqwoJdKV7XVrsVwO8nKQI66TkQmRxyCTW24kvAJ6zDmTfAFT55O+eQgveWJIiENrBTlskO331W8yaBNDrfUE3H8UpG43p975lLqnRZ9IoHpuzYgJwEM/APZj8UEp+o0ba/DGMfvFKLpCDpNl1gEFQQnTyqgw060tcsPPSKTKzr9Q7i3rj1EVvdP9dta24cOVOjJHT3wr+lG0tcVjPjUGnXmyCHXkGk6vFjA1OHDAwK+fH6ldmSKgQb0uW9LOTX~-1~||-1||~-1; JSESSIONID=0753DE53D690C22EE8D41C9E0EC9B60A; bm_mi=F942A40E103769AC501A96A563B4F018~YAAQLiZzaGEjcmyLAQAACCMRehV1L/TnkY5qY/2O222Tc/6g9flpAe0YImmuDJMOe01KNPSq0lYMpPCDPrMWfp821pnU2MtCFqO2GEIjO50fAwcUHfNAqtX2ADYKQ84wecwwq7yY8ysyWkDgBonbWohof2Pe/lgqVhfcky+ERJnFxSOOK7zAL34pf7yWhu6x25ex7VIerd3tjq+upR+NhlvqUXJXj6JxQUiTBtD5njIf33vbxRR7WezzIMLgsQ4gQCpP18/myRypVOlVc9753MTQ/AMAt81FvVomI6cESEclA2zAULg/OSHtRwH6R6Mte8WpDjBrOL56qN8zBxIcBMswHNsSrzMRpfTf7H6EestM~1; bm_sv=BC6C98A679C7A4C87C4DF2DE16A3F23B~YAAQLiZzaHAjcmyLAQAADCcRehXHbhVyO78TPi9PeTOLoXRLfJ1QVSxRGGl8/1iZLkPaOOrJ7VMhQRKx95HHys/Y4BLAuO5zftglhmFd5uAPcLl8wq3MUvIl0cUrWv82yTWdDAU6QIhkIn7HgpZJCA/Sg3KGzy/IuzBgn2obMIPaHzBAFTseWm5GWYLqicpq70UEn1u6UMOtbyDdA3LjIpgtPxs1DHbIhbNKRO+uiRLpBzl4hlUd8Z8TJdSEdRd1nA==~1; ak_bmsc=0B1FD08A0E3F25299775AB19EA0B2C0E~000000000000000000000000000000~YAAQLiZzaIIjcmyLAQAA7pQRehWIjGoT1+SzceudSFAUGO5LPGZ77kxr7ADuAdcbBFKV98FtE/qFnLV5qFFc7dmk8ENKbUDID1UpPzVnTGdMN8TfCursDyFiRfZmThagC0suzJvGAml9zpfxBKUr1x2GAVjwBXU2iwA6Bcykne+YfXXymh7Eoqsj4asVEq8u7+bIjm2IUHiUCKlIRUQn2yUEqQkJ2QyDxViD7jvNjNNn5NQRJS6vp646vIRhiLN0CygWG+owyWq1pCNf7fQHSfuiMU0Pyplt3GhoD1+7ntaiPDs4i4hzS43qFF8drL5CInN0UuFGcQ03f6TN23c9PLp4dnV44IqNuCDzfr1L8Sh3ew91AQHySLn+AhqObjbQfgxrNUCm0lD52v857TD7ovhix+bJXrtGgv8WivWgw0Fk0+BpwqiJHLOaLeJWTJDWav6aBMuqXBSwI3r2R6CYEpK/9ic=; _abck=9F748555848555FC89E1DCCDC2316EED~-1~YAAQ7V9idvfut22LAQAAB8cVegqOqvvE8ldLvIR7aHYaIbLP9Mez+5HnX2wDvuy0w6ykl5I2HiFWXFHEgb/fJTaTXIDrL/Nw47weIZwujYPjb5E4fAyFeANammnJlnkTXWAiWj/s9qYRDb6CMzyPDmy5ZuxEpFt79IMZogWXPOFlPD/wjvDs122dyFakn9OtxqoWwQLNwWn3b1pjff1l4xuQb/AXnU2UpFc7tpjhEVsxRCkx//6oZ331gFPDSTg4/kvvBrorjIwA9bjcwbUDsCJ1mkyekDtPgn3QqF1/Hqp4Q2Ws9S7USomZbwhE7sQYQVOq465/a7+V8u+NJXQrn1sUzXoH8LI3vhyfwvNpgJ/lNKbsUg6DZcad8Vbh7/LbcIXY8Ke4w+16gPWNWkVg2XIwlkwCxk0+~0~-1~-1; bm_sv=BC6C98A679C7A4C87C4DF2DE16A3F23B~YAAQHdxZJA6DHmyLAQAA22cSehW8CMDhPiwfrO068eESURorwP18iDR6y4vUysVDugIT3cv2d5zcvvJEi9SDf1c+LuJ7GEFlXlsRt5ki2D9E8DDrFQwKvoQ0XZJbBj8viLbgQ/IF15zIB83f8cqhXruMdpWuOBMlTFgQTtkIhVOlvjN3qLdC9VbGUxXVlQBiZ9DDB01esoadqY+0z33LeU/a3Lt8Y9WUkA/0cb9R3YuYBKzzMCVINiA+dD8NESneNQ==~1',
        "params": "[object Object]",
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
    pre_getListProductByShop(merchantCode, page)
    response = requests.request(
        "GET", url, headers=headers, data=payload, proxies=proxies
    )

    return response.json()

getListProductByShop('UFG-70003', 1)