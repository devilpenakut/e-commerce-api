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


def getAllCategory():
    url = "https://gql.tokopedia.com/graphql/categoryAllList"

    payload = json.dumps([
    {
        "operationName": "categoryAllList",
        "variables": {},
        "query": "query categoryAllList($categoryID: Int, $type: String) {\n  CategoryAllList: categoryAllList(categoryID: $categoryID, type: $type) {\n    categories {\n      identifier\n      name\n      id\n      child {\n        id\n        template\n        name\n        url\n        iconImageUrl\n        child {\n          name\n          url\n          id\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    ])
    headers = {
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'X-Version': '8ab2593',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'Referer': 'https://www.tokopedia.com/p',
    'X-Source': 'tokopedia-lite',
    'X-Tkpd-Lite-Service': 'zeus',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': '_abck=7053B61DF033355E32F25D33E634A7DA~-1~YAAQSGVVuGidPtKKAQAAP3lo5Aq1Ah8Xm6t243FHpaxKNt34vumOwPB9eI7xao4WdFh0FnpS8EICLpg8OKIuTXZtZklRY312BxzuoUUlmKhetQZs7nY2IF8MeBCosHZomm8jDGwVZIw8RpW1pBODinmYeFEzMODwr0wH4b6lX2Zr5G6SiWD4ZOdpCM7uL5M24jX5HLsRc+HfireFBRN7s1X4li5IBn5CLSMYksta5WJdlXExLhqXViXb9+H06rhaqkUcN2fB1orivbjV/6SSGklZvy/sj1JsUCkrGmwLtmOGElZuSjckyGfv8Ez8+WLwJjp/aF1ht7mz+T7xVIz2xMnWRJ9dWCvyyNCqQfDsrHmbemIBg5k8iufIGiCS4Vo=~-1~-1~-1; bm_sz=36F31EBF4A506B19C2247C7B9996C8F8~YAAQSGVVuGmdPtKKAQAAP3lo5BXR9ieeCks4ZMYNYA5pOOdyvx799qkQGJi7890yt/txwwcYLCxVJWAfPjbklJdHygIXd6bp0KNesJ9CP50uhMcmMpYm086CFSs1M7RIii9excPpTwktRM6bedDnWKYw/X1tWs+VsS9HI5V/Xf1m82z/luO3d5VQlGJJoLpIHNIj+E7VxSaLWsOfE7+RuI363m4vyVt5xZgcQaRid4C67QwnCCK7JgIAWE3CcZHf+gU7QO6AFB6puUMiGDfgfdjILwXd+vXCJFiW+cTlCfK5W8ovkQM=~3425842~3686724'
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

    
