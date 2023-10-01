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

getShopInfo("https://www.tokopedia.com/bajukoki")