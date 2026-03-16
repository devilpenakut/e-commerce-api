from .http_utils import request_with_retry, get_proxy
import random
import string
import re
import os
import json


def getAllCategory():
    cookies = {
        '_gcl_au': '1.1.1891895509.1701783434',
        '_fbp': 'fb.2.1701783434489.1686241188',
        'SPC_F': 'Il0ulPoXZqsK1tAOugZN03bgJJBX74Ol',
        'REC_T_ID': '66ef55d8-9373-11ee-ba74-8a1d7cb66d3e',
        'SPC_R_T_ID': 'x/HMdxjHmlM7fjKGzIeXhg5jwqoZjj2E0LrfB6I6LnQT6N59yMiL0YbCwrDGHnLft6EW0BakaQ0vlz8zYtpDawdloCQ93wjeqoPuz4ivrSxgr/UvhsdmkA/uauBgwahCx7Iu3o7KwzWgrZnXSIYcVcR2EQeskN6loWsCmDXA31s=',
        'SPC_R_T_IV': 'NjZMZzRlMGNBaURZUFdMMg==',
        'SPC_T_ID': 'x/HMdxjHmlM7fjKGzIeXhg5jwqoZjj2E0LrfB6I6LnQT6N59yMiL0YbCwrDGHnLft6EW0BakaQ0vlz8zYtpDawdloCQ93wjeqoPuz4ivrSxgr/UvhsdmkA/uauBgwahCx7Iu3o7KwzWgrZnXSIYcVcR2EQeskN6loWsCmDXA31s=',
        'SPC_T_IV': 'NjZMZzRlMGNBaURZUFdMMg==',
        '_med': 'refer',
        '__LOCALE__null': 'ID',
        'csrftoken': 'HgwqNMfE6etVqv7uh01koEA0RXtZmdQM',
        'SPC_SI': 'in6nZQAAAAAzRElHWFRhUf+VRAAAAAAAUXJRNUc4bWE=',
        'SPC_SEC_SI': 'v1-UERTQ1ZjeHprTkdFRGRyeZiX2s2+Q+4jafmA5ZQ1H7L2q1TBq0QWIEagJaTbTPEVVYHHny6Lupxvhy+VXi4FFK2tWn2eQjXMXHdimCjyKyk=',
        '_sapid': 'da8acc93b59a5cf6985957d49562d7170a95800f5933c353ab21ecfd',
        '_QPWSDCXHZQA': '3e3bd465-c9b0-4896-a738-0b3dd0364c43',
        'REC7iLP4Q': '3484444f-0b79-4d3c-b930-3593ada2403c',
        'shopee_webUnique_ccd': 'YSs0E2LfGMS%2BatGdMPvUrQ%3D%3D%7C4TrUM8JjwhNbExajBj%2BWXMdFaU5Iyuv1ohuu0KyNMVZQAzEW%2FZldDtvql5oCdD9XMmRdlhhuQ2A%3D%7C3142e3RmCjrSXLpE%7C08%7C3',
        'ds': 'c3b513a9ee164336fa5374ca605242c5',
        'AMP_TOKEN': '%24NOT_FOUND',
        '_ga': 'GA1.3.1514257641.1701783437',
        '_gid': 'GA1.3.1530549160.1705847267',
        '_dc_gtm_UA-61904553-8': '1',
        '_ga_SW6D8G0HXK': 'GS1.1.1705847267.17.1.1705847683.51.0.0',
    }

    headers = {
        'authority': 'shopee.co.id',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'af-ac-enc-dat': 'AAczLjQuMS0yAAABjSxyAn8AABBPAzAAAAAAAAAAAv+Jk48S5p7olfvwn34XQN5E76dIl/82EyfDx/bVRcPaaRvYm5f/NhMnw8f21UXD2mkb2JsWVRlkSYswZramTBKLBGV5COLCKOCc4aNfMACbUR0zV4RLEedzdpFZODbV1jHSSnRtDNtqq/e/6kR7vm7Wl9T+UXqGJJAo90NeTKUNDdltyeBp7apehbLI9qPtX0VpbIEhSvsYMlPrYirRCvm7NH4vcVnssygvj9h0nD8jdiN9rvJ7voJ8XJeMXIZnGp9TOCJMS6fkQk+1v73bZiAym3eMVlZMsmFPZIz0G593WgeSikhyQ7SnzE0Lr226YZbDVp6MZnIirB8O/gU8+Fz5LFlIdvrx2cDNAh/WiazMgcgB2IpWoI3lzvoPKDx96WVQBxHfn3ef+xokLITc0bqLihdVUQJfq3K1AG1EpKO616ktiwbY7P9KHML6aQtF4FlKd6xjdVpA6a7RMwH/8HLpttFgUQJfq3K1AG1EpKO616ktiwbY7P9KHML6aQtF4FlKd6wdA86fQ2w9qjRqJCAkbVT4rpOskOT93hbrDw1V+S5ojQsNXts5GyAjI8vnGItu2NNhh/wm6gMaLnkSZfhLSUaJN5NwO1tj5RgI6LeacDwoJwsNXts5GyAjI8vnGItu2NOGokCjTkYk4XwHiJy+vmLytYrArjVGC7NJynAhU8uaTnAA7DTjpRolFcqNFJ3yKO0pKTAu2oaTT1xzItRyGH9y+3I4j48xblhn1oq7tDjE5X3tZDzoJy5otCTMjGw0G8Vl+SEFWxwZ7ywqOZEULB4WQ+psbTVhZmNUMoHNLC1NzuXfq8xO+ZPo6VoSxJN3dktWjBbXtmMrXbHDkTP+1CbfJFaRA4xm5vEpqBbWqSvrMlpeRewmON+Rihy/oFyTjnqX/zYTJ8PH9tVFw9ppG9ibNYV5sig2iNQLAjv/komK+YPNwAc4MetWZmPrtGAoHxDi4KCKwVjuibyQk9eubMiONWA4pXxunM9TdmoFM/eJWx5VAm81dqWXUsVv1hb8bc/omC9sx4VlzjDZiiU4fFYBT14xBhlstwzFVbpGSg7Ptha5nzG0SHEwEt9pZ83BZD0=',
        'af-ac-enc-sz-token': 'YSs0E2LfGMS+atGdMPvUrQ==|4TrUM8JjwhNbExajBj+WXMdFaU5Iyuv1ohuu0KyNMVZQAzEW/ZldDtvql5oCdD9XMmRdlhhuQ2A=|3142e3RmCjrSXLpE|08|3',
        # 'cookie': '_gcl_au=1.1.1891895509.1701783434; _fbp=fb.2.1701783434489.1686241188; SPC_F=Il0ulPoXZqsK1tAOugZN03bgJJBX74Ol; REC_T_ID=66ef55d8-9373-11ee-ba74-8a1d7cb66d3e; SPC_R_T_ID=x/HMdxjHmlM7fjKGzIeXhg5jwqoZjj2E0LrfB6I6LnQT6N59yMiL0YbCwrDGHnLft6EW0BakaQ0vlz8zYtpDawdloCQ93wjeqoPuz4ivrSxgr/UvhsdmkA/uauBgwahCx7Iu3o7KwzWgrZnXSIYcVcR2EQeskN6loWsCmDXA31s=; SPC_R_T_IV=NjZMZzRlMGNBaURZUFdMMg==; SPC_T_ID=x/HMdxjHmlM7fjKGzIeXhg5jwqoZjj2E0LrfB6I6LnQT6N59yMiL0YbCwrDGHnLft6EW0BakaQ0vlz8zYtpDawdloCQ93wjeqoPuz4ivrSxgr/UvhsdmkA/uauBgwahCx7Iu3o7KwzWgrZnXSIYcVcR2EQeskN6loWsCmDXA31s=; SPC_T_IV=NjZMZzRlMGNBaURZUFdMMg==; _med=refer; __LOCALE__null=ID; csrftoken=HgwqNMfE6etVqv7uh01koEA0RXtZmdQM; SPC_SI=in6nZQAAAAAzRElHWFRhUf+VRAAAAAAAUXJRNUc4bWE=; SPC_SEC_SI=v1-UERTQ1ZjeHprTkdFRGRyeZiX2s2+Q+4jafmA5ZQ1H7L2q1TBq0QWIEagJaTbTPEVVYHHny6Lupxvhy+VXi4FFK2tWn2eQjXMXHdimCjyKyk=; _sapid=da8acc93b59a5cf6985957d49562d7170a95800f5933c353ab21ecfd; _QPWSDCXHZQA=3e3bd465-c9b0-4896-a738-0b3dd0364c43; REC7iLP4Q=3484444f-0b79-4d3c-b930-3593ada2403c; shopee_webUnique_ccd=YSs0E2LfGMS%2BatGdMPvUrQ%3D%3D%7C4TrUM8JjwhNbExajBj%2BWXMdFaU5Iyuv1ohuu0KyNMVZQAzEW%2FZldDtvql5oCdD9XMmRdlhhuQ2A%3D%7C3142e3RmCjrSXLpE%7C08%7C3; ds=c3b513a9ee164336fa5374ca605242c5; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.3.1514257641.1701783437; _gid=GA1.3.1530549160.1705847267; _dc_gtm_UA-61904553-8=1; _ga_SW6D8G0HXK=GS1.1.1705847267.17.1.1705847683.51.0.0',
        'if-none-match-': '55b03-158a0f98f80a09649f8dcfd2f8d263d4',
        'referer': 'https://shopee.co.id/Perlengkapan-Rumah-cat.11043778',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-api-source': 'pc',
        'x-requested-with': 'XMLHttpRequest',
        'x-sap-ri': '842bad65dd11655144160f320301fc7f23fc4cba0483e8848632',
        'x-sap-sec': 'dhufvsbRxcbcbcbcamb3bcVcambcbcVcbcbdbcbc7czcbMVRbcbMbcbc20sqOF6cbcbgbmbcCczcbRA1eENb65aDlUjmXsVTwUimYt831R7aexK+9tdhHl2pRgxjR5sGZAJ8IKID/oxxMCinxqP8nvvPYdk7OHCVXHVS1wCrGRI5bP49aMsxwh/kmT8WglPXDDgqc+fgxmhH+r+FT8GLqygpWIde6wA70VihVTiD4eGaooup7rN+RSz9jAGvN80V5nUhDePnXXWm7xj4im1pO/SUha5cTIafZvGNkwrR4qA9xjcESpOJ4sfDyju5w2EczlIA28cXZXEyz+v+36di9DWdJdLRtZioF7xsQTIn4kBFjBDwN+QLzKtYhrkPLzr5bX1E+O0/K0/+obl0tpw+qdO9pEDQ59+iWwPEwogZgZtyDDANYvZM+tFCx6eDGbhVXlX46/F1i6DTOytf0/MKhVcFfLeZtZeW+txo7SxKoLqZAv/lrS3M1Qvql/TJPjeUxuJb/vff2co0ot7Mj8V1YaFQ+87m8eHXkZX/VwiHPnsrVOSH/bjwOf68S9yuVCH95gjfebYhbZD8+eZ2PiZOr5UHd9t/Sx9kdg9pKArPEXJX2JjSFpksOJcrp7QKNLFSG3a7zW7q5JLCBonqcFHhe79t0KbK3hnYITlz6QaeVd2PksuZlqIdupS9tDfV7QD9+NDiqgjGshnBMJ0qLkbf0PukGW5TtDmoDFstOhXJO08auoDhBFpie6LEEmDQxMZYqSB/fvz+SSTzxp96YUnZTsekhg6Eim6cbcbTAT1gjjV8AmbcbcxLOqOqZcbcbQHcbcbPbcbcDs15FTbc5UsaZarVczJZ6UpmY+w3bcbcgrTzjT6XATXcbcbcZcbLbc6cacb3bcbcZcbcbQHcbcbPbcbcS2gkAdraBl/Nlzgy6aVqsJs7axR3bcbcjjqyTyX8jyzcbcbc',
        'x-shopee-language': 'id',
        'x-sz-sdk-version': '1.6.14',
    }

    response = request_with_retry("GET", 'http://147.136.167.34/api/v4/pages/get_category_tree', headers=headers)
        # print(response.json())
    print(response.json())
    return response.json()


def getAllCategoryLevel3(level2ID):
    # data = getRamdomPhoneModel()
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
        "match_id": level2ID,
        "page_type": "search",
        "scenario": "PAGE_CATEGORY",
    }

    response = request_with_retry("GET", 
        "http://147.136.167.34/api/v4/search/search_filter_config",
        headers=headers,
        # proxies=proxies,
        params=params,
    )
    # print(response.json())
    return response.json()
