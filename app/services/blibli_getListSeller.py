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


def getListSeller(NamaToko, page):
    start = (page - 1) * 24
    encodedKeyword = urllib.parse.quote(NamaToko)
    url = f"https://www.blibli.com/backend/search/seller/baju?&searchTerm={encodedKeyword}&page={page}&start={start}&showFacet=true&channelId=web"

    payload = {}
    headers = {
        "authority": "www.blibli.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        # "cache-control": "no-cache",
        # "channelid": "web",
        # "cookie": "Blibli-Is-Member=false; Blibli-Is-Remember=false; Blibli-Device-Id=U.5f0f2d1c-1fcb-4ca4-96fb-0a3bf801c9f3; Blibli-Device-Id-Signature=c30998000358b19d23c79431a3fd0b8d43e0189f; Blibli-User-Id=f0cdd9c5-354d-47b8-83c8-800f336d6aaf; Blibli-Session-Id=e79d6177-b91c-48de-89db-0d494196b560; Blibli-Signature=4ff8014901beaf38d68ca9aa52649ed015833c3c; Blibli-dv-id=JD_-h9VUxaOfzZlpwObqFlBW9-8QAmWgDaKbFOxV8Rk6vd; Blibli-dv-token=JT__btDmpLSYfIihBHi6ZT75KZh1M9x6pkK9kjuhzGOi7D; Blibli-dv-id-version=2; JSESSIONID=73F4D7A62C6EA10E52C06DEF7814ADCD; ak_bmsc=77D7091743D95C2271E026172257F086~000000000000000000000000000000~YAAQLiZzaIxbdWyLAQAANk2+ehUxxxXApWYSSQ1Zcz1g3jQowUj2tbNruLFgaExfwFnzZWapS4PKbovPQNpFzXde61BPBOd1EKCYwG6UyaZ3dIzcJMMPaAOeM5WhLNYW73xLLLNrUA2DZ/Dp9XVUwqCEgy+Q1HoU0xOdjhNmQJ04IsEpFYaV2mciA2XJ60uddNymDii26EGhaZeDkeYVmyxmDp4sxU5T56n/CzNFtM8O6OpBtuj8Ojmkio67Opk/y+k+y+CTnGfo+ZzvULs5Ta9bRNUHYBWAxiwHbO9QwrAt5fs6BXOvT0LgLie9Xiavm+Fk4HR37vY5nA5qlsmetvqNHWcG1oFDJ3/SX+/Gwj+qTTgzAG8d7yBLXQE86UncAlAIGfLxudsWOHw0; _abck=9F748555848555FC89E1DCCDC2316EED~0~YAAQLiZzaOKDd2yLAQAAsIntegptOsnX129chGNQGjAMyO1mIMnTJd1Yya0B6NRqGJyHAhbb8dxnA/Xp5AKHzdLISR0IonTRaDsJGFlIt2azTgAWiF2Lczv2iXnmJG0u0DeA64OnJkNCjE6oOLBmYTbJvN7tQIwtneWdJe3BBVUDOQUoDAnYHl1N/WpxitMRyB2xeYtflCki9tyMgm4cbHlRYjwtXrG1csPsQ0LNTIO1fFnLyswwuC584YmuFoQmE2xGRpwuiLcQWocASokCVkC3hFFvvBUyqhQ0SAkPlVTuVGejQyiaZLdLa2okwsn4ox/TZiZeZAcp3S72u+twSiyvonZ3ZQsz5UpD4PwT/XC2eJeAvXT2vLSCm6f/h3HQNhq02MJHlgewjDmvHcHcW7v2ChBoeKXC~-1~-1~-1; bm_sz=736C52F6D5158A82E419535FAD58F4B2~YAAQLiZzaOSDd2yLAQAAsIntehW2/sbERvOrcO1z9R0oI7pWwWJIiTZFUA5aGC6xxT9GqfMKHfzQ4vwUXXbvzf6gSdclM4mPzbxjAxbrf0PD9PLlDvNRdn9t3FBWfbOP7osFzUp/k3W6S/ji260acZM6dEXvmaKSk6xCn0tExn0EDEvUZ+PVX7Lg91Q+cKUZeLBNebAbo9y1VdCYru9Get/m2Vr8mYX0eJBsn56lC+bJ0smupONB1ocVy/Vth7owus1DA9YqI6MWSfSGY6Z5hLWuYzzS/3QrDY7NWWctzlhnHsQ=~4535619~3356228; AKA_A2=A; bm_mi=6CE689C3347CD5557249222B08A95C97~YAAQLiZzaBqQd2yLAQAAej3uehXdp+PoiXX6TA0widag4X26lo3dUDCsJaV+AWnVNBQzhh0GQbMxA6DK9/pKv4U6/NAQQ42x8q9+yoWUsJoYb+QmJf+d7PVVvjLKz7AEf2ia4wI9x/kAXvc4cM+iHbJYHWo3N0PVuc+vLxNuv8JKiJPSJCb8ZCLe1BOU2tXD9s5bkd/IjAPBZ8BXBG02pax/OlxYGEBQfw0qCCD0RomdUOXjUbJIq5LEETQTqpXpYROtOf4SW2zC+VqO4I+m/o7+k0+h4KcU/AiXyoLpxJ3H54CWlgRpGeS9LAnlhK4sBz2fBD4kSrd2FSghe9Cafq2/jYtLkRCXJc+ommLQ5w==~1; bm_sv=63C410FB70F009743FC7E9BA265042E6~YAAQLiZzaF26d2yLAQAA7ZHwehVpnnRTQHz3UsUtg8IiYREbjTZP9YvIuHIEYt/EsObr8VZ2CsU+v3SH01zYAL/C0QuDctnrRmZ26g2Y3uWMhi9+MF9aHuZf2o7HwFr3pg08L6nVLQCMAPSoGyGlrEgcvNwrmnfRlBSyRVTwl6mYN0BXo60KJsvevSFwaeEjCKsx7DYO8C0602T/hq9y9RPlB1UcnHXaILoIZJr+2F4sxT9/OXYs0ezQmp04NercYw==~1; _abck=9F748555848555FC89E1DCCDC2316EED~-1~YAAQcugyFwBJ9mWLAQAActXwegpT14qhfc6OZnCyTgIMjfgP34PMHmBVwoHaBdAn7UgxIEREdrJtTgZrqDHO0lcEdo4RzFTLCBWY1QFD3lBaWI8yLsF6rPmOKeXwau/qgj8VVirezzZLkDfOuXHqyNF1wkV66MnupAmOufoW5wg+xYtY9UKmFU5bHV4EyJi6uV0mJ0U0OjpLZxHgMX40rg+5vILOkylfi08UoodML3fiA2xkD+YYn0xxT/E5/0xoly8n0mIn9qjgVQuy7JC2/Yp2Gd5Ubw2a+SN7hw41b4NhCBRDZdTQ4UMVP8odyeSf9on8Nit3cLDzWJOUbmYmlH5suCN3rnZw2WvIvduRt6hyrcJOB+dT/K3+pMB8/9IDNeoLxv/g7csCyhs9mqvuRrloH+8n82DW~0~-1~-1; bm_sv=63C410FB70F009743FC7E9BA265042E6~YAAQcugyFwFJ9mWLAQAActXwehVtYZiwL7IAsqNlyS0NoTuyx6wptlrK9G15NRkPLS42FiYLFdMgtWPHJwwIGFY1oF5+RO3UgcyL0A5yD0Y1JU0ukLXwSi9AJCGx4K9HKuKudhOC5bBC3OYP2kCIlFOOMWbukq17oGbC4gEP/2uDMqh8g6SM4vtxvTkShSaxuj3ye3RGe+kYQVBmCpTd3nEfst8eTvKF6zG8kNBN5eci7frNeJah5S3s0eM3ZlIQ4Q==~1",
        "params": "[object Object]",
        "referer": "https://www.blibli.com/toko/cari/baju?searchTerm=",
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

    listSeller = response.json()
    listSeller = listSeller["data"]["sellerCatalogs"]

    return listSeller
