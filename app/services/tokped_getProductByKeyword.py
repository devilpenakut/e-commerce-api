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



def getProductByKeyword(page, keyword):
    url = "https://gql.tokopedia.com/graphql/SearchProductQueryV4"
    keyword = urllib.parse.quote_plus(keyword)
    start = (page-1)*60
    payload = json.dumps([
    {
        "operationName": "SearchProductQueryV4",
        "variables": {
        "params": f"device=desktop&navsource=&ob=23&page={page}&q={keyword}&related=true&rows=60&safe_search=false&scheme=https&shipping=&source=search&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product&start={start}&topads_bucket=true&user_addressId="
        },
        "query": "query SearchProductQueryV4($params: String!) {\n  ace_search_product_v4(params: $params) {\n    header {\n      totalData\n      totalDataText\n      processTime\n      responseCode\n      errorMessage\n      additionalParams\n      keywordProcess\n      componentId\n      __typename\n    }\n    data {\n      banner {\n        position\n        text\n        imageUrl\n        url\n        componentId\n        trackingOption\n        __typename\n      }\n      backendFilters\n      isQuerySafe\n      ticker {\n        text\n        query\n        typeId\n        componentId\n        trackingOption\n        __typename\n      }\n      redirection {\n        redirectUrl\n        departmentId\n        __typename\n      }\n      related {\n        position\n        trackingOption\n        relatedKeyword\n        otherRelated {\n          keyword\n          url\n          product {\n            id\n            name\n            price\n            imageUrl\n            rating\n            countReview\n            url\n            priceStr\n            wishlist\n            shop {\n              shopId: id\n              city\n              isOfficial\n              isPowerBadge\n              __typename\n            }\n            ads {\n              adsId: id\n              productClickUrl\n              productWishlistUrl\n              shopClickUrl\n              productViewUrl\n              __typename\n            }\n            badges {\n              title\n              imageUrl\n              show\n              __typename\n            }\n            ratingAverage\n            labelGroups {\n              position\n              type\n              title\n              url\n              __typename\n            }\n            componentId\n            __typename\n          }\n          componentId\n          __typename\n        }\n        __typename\n      }\n      suggestion {\n        currentKeyword\n        suggestion\n        suggestionCount\n        instead\n        insteadCount\n        query\n        text\n        componentId\n        trackingOption\n        __typename\n      }\n      products {\n        id\n        name\n        ads {\n          adsId: id\n          productClickUrl\n          productWishlistUrl\n          productViewUrl\n          __typename\n        }\n        badges {\n          title\n          imageUrl\n          show\n          __typename\n        }\n        category: departmentId\n        categoryBreadcrumb\n        categoryId\n        categoryName\n        countReview\n        customVideoURL\n        discountPercentage\n        gaKey\n        imageUrl\n        labelGroups {\n          position\n          title\n          type\n          url\n          __typename\n        }\n        originalPrice\n        price\n        priceRange\n        rating\n        ratingAverage\n        shop {\n          shopId: id\n          name\n          url\n          city\n          isOfficial\n          isPowerBadge\n          __typename\n        }\n        url\n        wishlist\n        sourceEngine: source_engine\n        __typename\n      }\n      violation {\n        headerText\n        descriptionText\n        imageURL\n        ctaURL\n        ctaApplink\n        buttonText\n        buttonType\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    ])
    headers = {
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'Tkpd-UserId': '0',
    'X-Version': '8ab2593',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'Referer': 'https://www.tokopedia.com/search?navsource=&page=2&q=baju&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=',
    'X-Source': 'tokopedia-lite',
    'x-device': 'desktop-0.0',
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
    
    
# getProductByKeyword(1, "baju")