from .http_utils import request_with_retry, get_proxy
import re
import os
import json

def getVoucherListQuery(shopID):
  url = "https://gql.tokopedia.com/graphql/VoucherListQuery"

  payload = json.dumps([
    {
      "operationName": "VoucherListQuery",
      "variables": {
        "shopID": shopID
      },
      "query": "query VoucherListQuery($shopID: Int!) {\n  getPublicMerchantVoucherList(shop_id: $shopID) {\n    vouchers {\n      amount {\n        amount\n        amountFormatted: amount_formatted\n        amountType: amount_type\n        __typename\n      }\n      inUseExpiry: in_use_expiry\n      minimumSpend: minimum_spend\n      minimumSpendFormatted: minimum_spend_formatted\n      owner {\n        identifier\n        __typename\n      }\n      status {\n        identifier\n        status\n        __typename\n      }\n      validThru: valid_thru\n      voucherID: voucher_id\n      name: voucher_name\n      voucherCode: voucher_code\n      voucherType: voucher_type {\n        identifier\n        voucherType: voucher_type\n        __typename\n      }\n      banner {\n        desktopUrl: desktop_url\n        __typename\n      }\n      tnc\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
  ])
  headers = {
    'authority': 'gql.tokopedia.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'cookie': '_UUID_NONLOGIN_=2c7bcae6f451d30e3b19d2d2b752eb59; hfv_banner=true; DID=bb1d6975b69e1507c93275bcd893c227c96e9288207821c88712f94af61a4ec4cd16930d367a5aa648a849aa9e23691a; DID_JS=YmIxZDY5NzViNjllMTUwN2M5MzI3NWJjZDg5M2MyMjdjOTZlOTI4ODIwNzgyMWM4ODcxMmY5NGFmNjFhNGVjNGNkMTY5MzBkMzY3YTVhYTY0OGE4NDlhYTllMjM2OTFh47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; _gcl_au=1.1.888532133.1691863641; _UUID_CAS_=2486df42-6f41-454f-98c0-d8f1aeb0072a; _fbp=fb.1.1691863646763.357865637; _gid=GA1.2.613837028.1697595533; _SID_Tokopedia_=ux1RhJvQK86PPrghUv02nNIl72f1j0R6zces2zP5-W1Nohu0RcGmZr0cM8WSRZM8oaoH6H9TpSW543TUTLy8ItwBEfMlrwczwYY7pqB6Yp557i94ICtBKDVPac-WXcu4; _CASE_=2a73351835736b636366657d73301835736b617d733d333d736b731b303a30232530710124223025737d73321835736b6066677d733d3e3f36736b73737d733d3025736b73737d7321123e736b73737d73261835736b736063636061626664737d73221835736b736060646261646662737d732205282134736b736339737d73263922736b730a2a0d73223423273832340e252821340d736b0d7363390d737d0d7326302334393e2422340e38350d736b0d7360636360616266640d737d0d730e0e252821343f303c340d736b0d7303343723342239042234231d121006302334393e242234153025300d732c7d2a0d73223423273832340e252821340d736b0d7360643c0d737d0d7326302334393e2422340e38350d736b0d73610d737d0d730e0e252821343f303c340d736b0d7303343723342239042234231d121006302334393e242234153025300d732c0c737d733d042135736b73636163627c60617c60690561686b60696b64627a61666b6161732c; _abck=5B20CA345FC4340AB12F966B5211C853~0~YAAQzS2pyqDWH0GLAQAA4rHkQQqZvcOvFppjC+A49b5M6tK1b204eOkIAeB79DhhWNQS1Nq9DbvMq6P5EP5cxn9HtvUoh3prDM1qShyGZoNM6QcYo8nB9L9f5qGJsLukZ7XzzvjX+pAxXuOHRZ7TZk99+ZpO7CqXD7Pn+SSmhzLCuzoWWPRswuJXIPI0i/hnU4H/dRhONvVBxSsK5aKod5Zk84By/y1XPkPivikK6+t+V914gzTlfU43Fro2xiiTIpPBGL/leESShX/BJl3uZXOR8lHiI+cNwbweEkHJkJTQlIOc0pgne4SlJGx6tU72q0H1l3uvFAAXPpaI7rd+/z6Z2NbO+WBwkfCjDjaH6ClFDLC8ViVStxBqUsNOhkLcKIiQAVh7MDljZVZHFGnhR5msc0N5EdO8F7+q~-1~-1~-1; AMP_TOKEN=%24NOT_FOUND; ak_bmsc=642FD03FDA1DC8E3ADE2943FC1057EAC~000000000000000000000000000000~YAAQ5y2pylp3CzuLAQAAmwbnQRXADasffTX0Pw7ehvRm6iNRHfnJ4EvqKVRQ1VO0MLE5vxb0kp8whZamrEL7dSQQ83sIJkE10+8wSAoSEWTEsSYZBWhqQyjZ39j0RZZH9totQ1Fm0WRTBrAWXhHBYbBvNDUk/VQzphZer69cg6IpzXmMjz/hR47v4ZTVU6+cVAtfSUIAwrS5s6QzgcfAyeQP4PkexB4GZi69VaK/fxMk6qlGlCzutKu+s8H8o++OS5MhKhLTpb/m6PU11Didb7KZoLQMwbb5jGmWjKZDQ+TZnBNSx7vqe+D86XRlqxQ/85HnH5W8/F13xsdCiG6IXZdKD4l3KPYdIDAQP+XMBf6CY+3h+h35UmwW2ZIkEDT/LEDUD4YyudUJ2aUrCzs=; bm_sz=AD130B0FC3FA20FF021BB782AD3600BD~YAAQ5y2pyr54CzuLAQAARo3nQRW10N5KbkYsyusoQA0nKBVaqEp0cg0nZYUDNdVP+6/cUlL1fi9lr0K3C1kVeExPplHftSaefLx0jtN4ZvvTqJKYJDk1GLI7lZ8mcgfEGKH5dF+eItA5z2ZTfa4H9+PEvo3PfGDlCLRePRob3DnuWNeGuL+kCZzHh6hoPMsBXc1XH34dwVkOknglarzur9tmXVu7Xv9vw0wxuXiYg4NRlMUGuKM5cGCep+uxrtmcOO4qc0JERq++W4dNc7YuLBjWTHofXQlLVa42+bNpPewmPEp31uc=~3683393~3421505; _dc_gtm_UA-9801603-1=1; _gat_UA-9801603-1=1; _dc_gtm_UA-126956641-6=1; bm_mi=E098CE3E048B2591960E5BA6CA1FC621~YAAQ5y2pynJ7CzuLAQAAf5joQRXPDlgbAdk8bjLTCsdEa5GpkbSBB83Hf0L0+uFO1ZOy5x/RgXaMOhpFP2HepdTsIsSAWMez0hKQkljQ1n/pb75NWL9YlFHNTF7OsEb1dEsGSEwqr/FVViSa9ntbZJHWmH1G896y5J+dxDvRLhyojhpPtAw6rf4v831YzahugfoloH7harCzaaiyoQ43Pf3pEdOFIv8mrULAqJm9H04dGEB1Qo8haiYCzQctGHs0FY09eyUXndGS+VMmqwdFPTJEzZxj3bBEvcDRHDjGEmA62FiOGiPFMlETM+Xnw/Jm83w2eKQf47HGqLTd5P8I~1; ISID=%7B%22www.tokopedia.com%22%3A%22d3d3LnRva29wZWRpYS5jb20%3D.829784fb8de96400a9ae9b2f7322418e.1697617589905.1697598340765.1697617844111.6%22%7D; _ga_70947XW48P=GS1.1.1697617589.18.1.1697617845.52.0.0; _ga=GA1.1.282913632.1691863642; _abck=5B20CA345FC4340AB12F966B5211C853~-1~YAAQRWVVuKlqIjqLAQAApgjwQQrotCUxAXKpAIXatlkEBnxTfUsnnJC5Jsoz81lplgLT/APSdPFh9MpszQFzsd30bE5SmsVUBAkkIGFdwmsiwsC1xMIgc2T6oPNjI3WeKOLodfvYS1LlQS0I8LTzabbxIjV7O5+HbiZjr5bOmCWqq3zPIVbzUU3X/hbRQiNGyk4VZ7T5QwgH90nPREnmYSHD3ZZ7sPwrisHjBFN+P4WIBT4IQt9A/NOcBbJNN7YFIb9Z5ej5ps5CIbemhLxepQs3OH+yv4HfSD04UzZK5xW5UGfea69G0cCjVYB6VPVmD3RSji3R/cwFX39nRzJfjZcpJrma0RnAe7Sb2lDbJayTRPsEi6QddVwupW39xk1K4kv/cgN6XFmhefX/eCKnREqsPhqGvEFgr4tr~0~-1~-1; bm_sz=D350268BB4A25C9E0F0DEE98C93E65C4~YAAQRWVVuAxkIjqLAQAAsUDpQRWDuI+1G7hHL1Yquc7CJcx/DxW6OEB6Y6LnZ3s8qivrcCxjmoUowPhYPkga0IPnjBTsJ59PEL8xCXD5fZzpe+ZjeD1EnJf57XabALvxnJKtb5HUvly7Bu+VCnWcUy17GsE2COfElTr8ylusf/NNvHeKbmV7vSqEBah7eY8c/Pzi/CIufhRV2Wg1zN+QSqffOyoCwzNaHlpN1ppE/zh6dm+Id3bjIGJVVxzxvIkw6/xBaJc98DaRAaJUO95emcnxyGlOsV8kv+5DGMaVVd74mlQ39No=~3289143~3289653',
    'origin': 'https://www.tokopedia.com',
    'referer': 'https://www.tokopedia.com/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'x-device': 'default_v3',
    'x-source': 'tokopedia-lite',
    'x-tkpd-lite-service': 'zeus',
    'x-version': '8fd80b3'
  }

  proxies = get_proxy()
  response = request_with_retry("POST", url, headers=headers, data=payload, proxies= proxies)
  return response.json()

def getSpeedQuery(shopID):
  url = "https://gql.tokopedia.com/graphql/shopSpeedQuery"

  payload = json.dumps([
    {
      "operationName": "shopSpeedQuery",
      "variables": {
        "shopId": shopID,
      },
      "query": "query shopSpeedQuery($shopId: Int!) {"
                 "  shopSpeed: ProductShopChatSpeedQuery(shopId: $shopId) {"
                 "    messageResponseTime"
                 "    __typename"
                 "  }"
                 "}"
    }
  ])
  headers = {
    'authority': 'gql.tokopedia.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'cookie': '_UUID_NONLOGIN_=2c7bcae6f451d30e3b19d2d2b752eb59; hfv_banner=true; DID=bb1d6975b69e1507c93275bcd893c227c96e9288207821c88712f94af61a4ec4cd16930d367a5aa648a849aa9e23691a; DID_JS=YmIxZDY5NzViNjllMTUwN2M5MzI3NWJjZDg5M2MyMjdjOTZlOTI4ODIwNzgyMWM4ODcxMmY5NGFmNjFhNGVjNGNkMTY5MzBkMzY3YTVhYTY0OGE4NDlhYTllMjM2OTFh47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; _gcl_au=1.1.888532133.1691863641; _UUID_CAS_=2486df42-6f41-454f-98c0-d8f1aeb0072a; _fbp=fb.1.1691863646763.357865637; _gid=GA1.2.613837028.1697595533; _SID_Tokopedia_=ux1RhJvQK86PPrghUv02nNIl72f1j0R6zces2zP5-W1Nohu0RcGmZr0cM8WSRZM8oaoH6H9TpSW543TUTLy8ItwBEfMlrwczwYY7pqB6Yp557i94ICtBKDVPac-WXcu4; _CASE_=2a73351835736b636366657d73301835736b617d733d333d736b731b303a30232530710124223025737d73321835736b6066677d733d3e3f36736b73737d733d3025736b73737d7321123e736b73737d73261835736b736063636061626664737d73221835736b736060646261646662737d732205282134736b736339737d73263922736b730a2a0d73223423273832340e252821340d736b0d7363390d737d0d7326302334393e2422340e38350d736b0d7360636360616266640d737d0d730e0e252821343f303c340d736b0d7303343723342239042234231d121006302334393e242234153025300d732c7d2a0d73223423273832340e252821340d736b0d7360643c0d737d0d7326302334393e2422340e38350d736b0d73610d737d0d730e0e252821343f303c340d736b0d7303343723342239042234231d121006302334393e242234153025300d732c0c737d733d042135736b73636163627c60617c60690561686b60696b64627a61666b6161732c; _abck=5B20CA345FC4340AB12F966B5211C853~0~YAAQzS2pyqDWH0GLAQAA4rHkQQqZvcOvFppjC+A49b5M6tK1b204eOkIAeB79DhhWNQS1Nq9DbvMq6P5EP5cxn9HtvUoh3prDM1qShyGZoNM6QcYo8nB9L9f5qGJsLukZ7XzzvjX+pAxXuOHRZ7TZk99+ZpO7CqXD7Pn+SSmhzLCuzoWWPRswuJXIPI0i/hnU4H/dRhONvVBxSsK5aKod5Zk84By/y1XPkPivikK6+t+V914gzTlfU43Fro2xiiTIpPBGL/leESShX/BJl3uZXOR8lHiI+cNwbweEkHJkJTQlIOc0pgne4SlJGx6tU72q0H1l3uvFAAXPpaI7rd+/z6Z2NbO+WBwkfCjDjaH6ClFDLC8ViVStxBqUsNOhkLcKIiQAVh7MDljZVZHFGnhR5msc0N5EdO8F7+q~-1~-1~-1; AMP_TOKEN=%24NOT_FOUND; ak_bmsc=642FD03FDA1DC8E3ADE2943FC1057EAC~000000000000000000000000000000~YAAQ5y2pylp3CzuLAQAAmwbnQRXADasffTX0Pw7ehvRm6iNRHfnJ4EvqKVRQ1VO0MLE5vxb0kp8whZamrEL7dSQQ83sIJkE10+8wSAoSEWTEsSYZBWhqQyjZ39j0RZZH9totQ1Fm0WRTBrAWXhHBYbBvNDUk/VQzphZer69cg6IpzXmMjz/hR47v4ZTVU6+cVAtfSUIAwrS5s6QzgcfAyeQP4PkexB4GZi69VaK/fxMk6qlGlCzutKu+s8H8o++OS5MhKhLTpb/m6PU11Didb7KZoLQMwbb5jGmWjKZDQ+TZnBNSx7vqe+D86XRlqxQ/85HnH5W8/F13xsdCiG6IXZdKD4l3KPYdIDAQP+XMBf6CY+3h+h35UmwW2ZIkEDT/LEDUD4YyudUJ2aUrCzs=; bm_sz=AD130B0FC3FA20FF021BB782AD3600BD~YAAQ5y2pyr54CzuLAQAARo3nQRW10N5KbkYsyusoQA0nKBVaqEp0cg0nZYUDNdVP+6/cUlL1fi9lr0K3C1kVeExPplHftSaefLx0jtN4ZvvTqJKYJDk1GLI7lZ8mcgfEGKH5dF+eItA5z2ZTfa4H9+PEvo3PfGDlCLRePRob3DnuWNeGuL+kCZzHh6hoPMsBXc1XH34dwVkOknglarzur9tmXVu7Xv9vw0wxuXiYg4NRlMUGuKM5cGCep+uxrtmcOO4qc0JERq++W4dNc7YuLBjWTHofXQlLVa42+bNpPewmPEp31uc=~3683393~3421505; _dc_gtm_UA-9801603-1=1; _gat_UA-9801603-1=1; _dc_gtm_UA-126956641-6=1; bm_mi=E098CE3E048B2591960E5BA6CA1FC621~YAAQ5y2pynJ7CzuLAQAAf5joQRXPDlgbAdk8bjLTCsdEa5GpkbSBB83Hf0L0+uFO1ZOy5x/RgXaMOhpFP2HepdTsIsSAWMez0hKQkljQ1n/pb75NWL9YlFHNTF7OsEb1dEsGSEwqr/FVViSa9ntbZJHWmH1G896y5J+dxDvRLhyojhpPtAw6rf4v831YzahugfoloH7harCzaaiyoQ43Pf3pEdOFIv8mrULAqJm9H04dGEB1Qo8haiYCzQctGHs0FY09eyUXndGS+VMmqwdFPTJEzZxj3bBEvcDRHDjGEmA62FiOGiPFMlETM+Xnw/Jm83w2eKQf47HGqLTd5P8I~1; ISID=%7B%22www.tokopedia.com%22%3A%22d3d3LnRva29wZWRpYS5jb20%3D.829784fb8de96400a9ae9b2f7322418e.1697617589905.1697598340765.1697617844111.6%22%7D; _ga_70947XW48P=GS1.1.1697617589.18.1.1697617845.52.0.0; _ga=GA1.1.282913632.1691863642; _abck=5B20CA345FC4340AB12F966B5211C853~-1~YAAQRWVVuKlqIjqLAQAApgjwQQrotCUxAXKpAIXatlkEBnxTfUsnnJC5Jsoz81lplgLT/APSdPFh9MpszQFzsd30bE5SmsVUBAkkIGFdwmsiwsC1xMIgc2T6oPNjI3WeKOLodfvYS1LlQS0I8LTzabbxIjV7O5+HbiZjr5bOmCWqq3zPIVbzUU3X/hbRQiNGyk4VZ7T5QwgH90nPREnmYSHD3ZZ7sPwrisHjBFN+P4WIBT4IQt9A/NOcBbJNN7YFIb9Z5ej5ps5CIbemhLxepQs3OH+yv4HfSD04UzZK5xW5UGfea69G0cCjVYB6VPVmD3RSji3R/cwFX39nRzJfjZcpJrma0RnAe7Sb2lDbJayTRPsEi6QddVwupW39xk1K4kv/cgN6XFmhefX/eCKnREqsPhqGvEFgr4tr~0~-1~-1; bm_sz=D350268BB4A25C9E0F0DEE98C93E65C4~YAAQRWVVuAxkIjqLAQAAsUDpQRWDuI+1G7hHL1Yquc7CJcx/DxW6OEB6Y6LnZ3s8qivrcCxjmoUowPhYPkga0IPnjBTsJ59PEL8xCXD5fZzpe+ZjeD1EnJf57XabALvxnJKtb5HUvly7Bu+VCnWcUy17GsE2COfElTr8ylusf/NNvHeKbmV7vSqEBah7eY8c/Pzi/CIufhRV2Wg1zN+QSqffOyoCwzNaHlpN1ppE/zh6dm+Id3bjIGJVVxzxvIkw6/xBaJc98DaRAaJUO95emcnxyGlOsV8kv+5DGMaVVd74mlQ39No=~3289143~3289653',
    'origin': 'https://www.tokopedia.com',
    'referer': 'https://www.tokopedia.com/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'x-device': 'default_v3',
    'x-source': 'tokopedia-lite',
    'x-tkpd-lite-service': 'zeus',
    'x-version': '8fd80b3'
  }

  proxies = get_proxy()
  response = request_with_retry("POST", url, headers=headers, data=payload, proxies= proxies)
  # print(response.json())
  return response.json()

def ShopStatisticQuery(shopID):
  url = "https://gql.tokopedia.com/graphql/ShopStatisticQuery"

  payload = json.dumps([
    {
      "operationName": "ShopStatisticQuery",
      "variables": {
        "shopID": shopID,
        "shopIDStr": str(shopID)
      },
      "query": "query ShopStatisticQuery($shopID: Int!, $shopIDStr: String!) {\n  shopSatisfaction: ShopSatisfactionQuery(shopId: $shopID) {\n    recentOneMonth {\n      bad\n      good\n      neutral\n      __typename\n    }\n    __typename\n  }\n  shopRating: productrevGetShopRating(shopID: $shopIDStr) {\n    detail {\n      formattedTotalReviews\n      rate\n      percentage\n      percentageFloat\n      totalReviews\n      __typename\n    }\n    totalRating\n    ratingScore\n    __typename\n  }\n  shopReputation: reputation_shops(shop_ids: [$shopID]) {\n    badge\n    score\n    score_map\n    __typename\n  }\n}\n"
    }
  ])
  headers = {
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'X-Version': '8fd80b3',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'Referer': 'https://www.tokopedia.com/ichibot/product',
    'X-Source': 'tokopedia-lite',
    'X-Tkpd-Lite-Service': 'zeus',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': '_abck=5B20CA345FC4340AB12F966B5211C853~-1~YAAQRWVVuKlqIjqLAQAApgjwQQrotCUxAXKpAIXatlkEBnxTfUsnnJC5Jsoz81lplgLT/APSdPFh9MpszQFzsd30bE5SmsVUBAkkIGFdwmsiwsC1xMIgc2T6oPNjI3WeKOLodfvYS1LlQS0I8LTzabbxIjV7O5+HbiZjr5bOmCWqq3zPIVbzUU3X/hbRQiNGyk4VZ7T5QwgH90nPREnmYSHD3ZZ7sPwrisHjBFN+P4WIBT4IQt9A/NOcBbJNN7YFIb9Z5ej5ps5CIbemhLxepQs3OH+yv4HfSD04UzZK5xW5UGfea69G0cCjVYB6VPVmD3RSji3R/cwFX39nRzJfjZcpJrma0RnAe7Sb2lDbJayTRPsEi6QddVwupW39xk1K4kv/cgN6XFmhefX/eCKnREqsPhqGvEFgr4tr~0~-1~-1; bm_sz=D350268BB4A25C9E0F0DEE98C93E65C4~YAAQRWVVuAxkIjqLAQAAsUDpQRWDuI+1G7hHL1Yquc7CJcx/DxW6OEB6Y6LnZ3s8qivrcCxjmoUowPhYPkga0IPnjBTsJ59PEL8xCXD5fZzpe+ZjeD1EnJf57XabALvxnJKtb5HUvly7Bu+VCnWcUy17GsE2COfElTr8ylusf/NNvHeKbmV7vSqEBah7eY8c/Pzi/CIufhRV2Wg1zN+QSqffOyoCwzNaHlpN1ppE/zh6dm+Id3bjIGJVVxzxvIkw6/xBaJc98DaRAaJUO95emcnxyGlOsV8kv+5DGMaVVd74mlQ39No=~3289143~3289653'
  }

  proxies = get_proxy()
  response = request_with_retry("POST", url, headers=headers, data=payload, proxies= proxies)
  return response.json()
  
  

def getShopInfo(url):
  regex = r"(?:https:\/\/www\.)?tokopedia\.com\/([^\/]+)"
    
  match = re.search(regex, url)
    
  slug = match.group(1)
  # print(slug)
  
  url = "https://gql.tokopedia.com/graphql/ShopInfoCore"

  payload = json.dumps([
    {
      "operationName": "ShopInfoCore",
      "variables": {
        "id": 0,
        "domain": slug
      },
      "query": "query ShopInfoCore($id: Int!, $domain: String) {\n  shopInfoByID(input: {shopIDs: [$id], fields: [\"active_product\", \"allow_manage_all\", \"assets\", \"core\", \"closed_info\", \"create_info\", \"favorite\", \"location\", \"status\", \"is_open\", \"other-goldos\", \"shipment\", \"shopstats\", \"shop-snippet\", \"other-shiploc\", \"shopHomeType\", \"branch-link\", \"goapotik\", \"fs_type\"], domain: $domain, source: \"shoppage\"}) {\n    result {\n      shopCore {\n        description\n        domain\n        shopID\n        name\n        tagLine\n        defaultSort\n        __typename\n      }\n      createInfo {\n        openSince\n        __typename\n      }\n      favoriteData {\n        totalFavorite\n        alreadyFavorited\n        __typename\n      }\n      activeProduct\n      shopAssets {\n        avatar\n        cover\n        __typename\n      }\n      location\n      isAllowManage\n      branchLinkDomain\n      isOpen\n      shipmentInfo {\n        isAvailable\n        image\n        name\n        product {\n          isAvailable\n          productName\n          uiHidden\n          __typename\n        }\n        __typename\n      }\n      shippingLoc {\n        districtName\n        cityName\n        __typename\n      }\n      shopStats {\n        productSold\n        totalTxSuccess\n        totalShowcase\n        __typename\n      }\n      statusInfo {\n        shopStatus\n        statusMessage\n        statusTitle\n        tickerType\n        __typename\n      }\n      closedInfo {\n        closedNote\n        until\n        reason\n        detail {\n          status\n          __typename\n        }\n        __typename\n      }\n      bbInfo {\n        bbName\n        bbDesc\n        bbNameEN\n        bbDescEN\n        __typename\n      }\n      goldOS {\n        isGold\n        isGoldBadge\n        isOfficial\n        badge\n        shopTier\n        __typename\n      }\n      shopSnippetURL\n      customSEO {\n        title\n        description\n        bottomContent\n        __typename\n      }\n      isQA\n      isGoApotik\n      partnerInfo {\n        fsType\n        __typename\n      }\n      epharmacyInfo {\n        siaNumber\n        sipaNumber\n        apj\n        __typename\n      }\n      __typename\n    }\n    error {\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
  ])
  headers = {
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'X-Version': '8ab2593',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'Referer': 'https://www.tokopedia.com/',
    'X-Source': 'tokopedia-lite',
    'X-Tkpd-Lite-Service': 'zeus',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': '_abck=7053B61DF033355E32F25D33E634A7DA~-1~YAAQWGVVuKCaX9KKAQAABKr85grtGlqX+fULWL7hvHd9n9cHftc2VcdQHyKX057SNs0StAFyfWjsH2bZWSvjyz6+cl4A7TSgPko1hh98v3si8bGpC/vxZMxmVvk92uYKhohWp3DCz1K1vfNMcN6irN9Wo5C/m1PVXKHyPBBqLI9YYnFCNjDXop9fvYA+DPMdcTmmmgdCaApu25V9jkb9whLQkwDOzKg6h3doLXUR6OUfjOYvtpscVeQsLBzFVKuIqKv2UMc6BayUMozGRLlPbYrRhFp77nK1TdfVMvUt5FU1oNRD7dSnOjN7KbqIzCxvGShIINMGzBaguEMrtb1xZPl5DradJ1+q8EDG363j7AKbogC/0axLvBdLFnBTQ2/k1rkV9EGeZOoweHGaIg==~-1~-1~-1; bm_sz=79E03C9E011C3E7009F37BC9DE84076C~YAAQWGVVuKGaX9KKAQAABKr85hVcZgvGmYzlCIHn6un9DphhxL8cRIfWdGvdb2Xi9OX0XJAIh0Gu61moStOkirlZSZpgAWHyNhSyWwZkZqMFSIU/4ei84nQZayUZ6SL7YW7MRhw5U/89enm78L5YxkbXNOVoOLWpcO7Z0a+ieq9BVnLKTa9+cE9XVvy1uLwVJUqkhJpxeB9MwJXO1kAleZkSdBMcT5u384QTot7IGr+Trzki7fzCvdUAYSqNG+Zc6Vr0cc11A39EhG3XimOC9YWlg8wQYkyfQG3bHQn7NDXSnmVkvFs=~4601409~4604978'
  }
  proxies = get_proxy()
  response = request_with_retry("POST", url, headers=headers, data=payload, proxies= proxies)
  responseJSON = response.json()
  shopID=responseJSON[0]['data']['shopInfoByID']['result'][0]['shopCore']['shopID']
  # to int
  shopID = int(shopID)
  voucherList = getVoucherListQuery(shopID)
  statistic = ShopStatisticQuery(shopID)
  shopSpeed = getSpeedQuery(shopID)
  newRespon = {
    "ShopInfoCore": responseJSON,
    "ShopStatisticQuery": statistic,
    "VoucherListQuery": voucherList,
    "shopSpeedQuery": shopSpeed
  }
  return newRespon


# getShopInfo("https://www.tokopedia.com/bajukoki")
# getSpeedQuery()