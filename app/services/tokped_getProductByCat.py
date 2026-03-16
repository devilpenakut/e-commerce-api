from .http_utils import request_with_retry, get_proxy
import re
import os
import json
def getProductBycat(page, catId):
    start = ((page-1)*60)+1
    url = "https://gql.tokopedia.com/graphql/SearchProductQuery"

    payload = json.dumps([
    {
        "operationName": "SearchProductQuery",
        "variables": {
        "params": f"page={page}&ob=&sc={catId}&user_id=0&rows=60&start={start}&source=directory&device=desktop&page={page}&related=true&st=product&safe_search=false",
        "adParams": ""
        },
        "query": "query SearchProductQuery($params: String, $adParams: String) {\n  CategoryProducts: searchProduct(params: $params) {\n    count\n    data: products {\n      id\n      url\n      imageUrl: image_url\n      imageUrlLarge: image_url_700\n      catId: category_id\n      gaKey: ga_key\n      countReview: count_review\n      discountPercentage: discount_percentage\n      preorder: is_preorder\n      name\n      price\n      priceInt: price_int\n      original_price\n      rating\n      wishlist\n      labels {\n        title\n        color\n        __typename\n      }\n      badges {\n        imageUrl: image_url\n        show\n        __typename\n      }\n      shop {\n        id\n        url\n        name\n        goldmerchant: is_power_badge\n        official: is_official\n        reputation\n        clover\n        location\n        __typename\n      }\n      labelGroups: label_groups {\n        position\n        title\n        type\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  displayAdsV3(displayParams: $adParams) {\n    data {\n      id\n      ad_ref_key\n      redirect\n      sticker_id\n      sticker_image\n      productWishListUrl: product_wishlist_url\n      clickTrackUrl: product_click_url\n      shop_click_url\n      product {\n        id\n        name\n        wishlist\n        image {\n          imageUrl: s_ecs\n          trackerImageUrl: s_url\n          __typename\n        }\n        url: uri\n        relative_uri\n        price: price_format\n        campaign {\n          original_price\n          discountPercentage: discount_percentage\n          __typename\n        }\n        wholeSalePrice: wholesale_price {\n          quantityMin: quantity_min_format\n          quantityMax: quantity_max_format\n          price: price_format\n          __typename\n        }\n        count_talk_format\n        countReview: count_review_format\n        category {\n          id\n          __typename\n        }\n        preorder: product_preorder\n        product_wholesale\n        free_return\n        isNewProduct: product_new_label\n        cashback: product_cashback_rate\n        rating: product_rating\n        top_label\n        bottomLabel: bottom_label\n        __typename\n      }\n      shop {\n        image_product {\n          image_url\n          __typename\n        }\n        id\n        name\n        domain\n        location\n        city\n        tagline\n        goldmerchant: gold_shop\n        gold_shop_badge\n        official: shop_is_official\n        lucky_shop\n        uri\n        owner_id\n        is_owner\n        badges {\n          title\n          image_url\n          show\n          __typename\n        }\n        __typename\n      }\n      applinks\n      __typename\n    }\n    template {\n      isAd: is_ad\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    ])
    headers = {
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'Tkpd-UserId': '0',
    'X-Version': '8ab2593',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'iris_session_id': 'd3d3LnRva29wZWRpYS5jb20=.8333fc9d339ce4fa7b2a6af65ad76a41.1696076580108',
    'content-type': 'application/json',
    'accept': '*/*',
    'Referer': 'https://www.tokopedia.com/p/audio-kamera-elektronik-lainnya/baterai-charger-kamera/baterai-kamera?page=2',
    'X-Source': 'tokopedia-lite',
    'x-device': 'desktop-0.0',
    'X-Tkpd-Lite-Service': 'zeus',
    'sec-ch-ua-platform': '"Windows"',
    #'Cookie': '_abck=7053B61DF033355E32F25D33E634A7DA~-1~YAAQb3obuMHitM2KAQAAol0M5grMtRhOBBp5EbdWdj39XlbDi/hJ6gDsDtZ+HRweDi+gtWSxGpRA0IalucPetOXOkxOWWwpYiXkWE3EF/b/y7jR8Rx8jDieLl62hFaUjfdZAQ2Yb8Vz6gV02BYn9NJV+iKZXd2yFrQSVWF66mBlrGFeRBklDSSnzzv27o80zrnHIwasSvzfH6+zTSaP4erpYTwlJLdDeXCdaE445StprTWdla+YxWYM8RjTuArjeupuI+lHkqVtCAnUrhzvv8FfZ2JmyDrPGXhpXQnVWx2NXJbtE+YaF239qX1RyavIciT55ctyf5MoMLcsZcIXLI8z+zmtw1uJSLvquSm4XR8f4EMTfD8Wuz7X1ZYu7laKUMFQICwzXWPiWUerSrw==~-1~-1~-1; bm_sz=79839CC616FBCCE4A08EA88491ED8109~YAAQb3obuMLitM2KAQAAol0M5hVpCd0ops2mokNoabgXbDmpOs75Srag570HM4GrFMMJmFiI+5cSCrGFYpN9wZ6Kf8WMEcMVxoiEvq700Pcr6hMb3sd8NlCV/QAFjq1sSQ2+4tLsgR4q2TucBcsZ7Xq0mg6X38+E8Ym9uhGyu3jZkoyNqQe4ToPePDXXW0VO7bmzCkXLBHq3YdpT7usToONUQd/lXUplc4dYcrvSr8ZzzIIaatLr2e9lKXfvh3U/YGF95R6tI1zyaP9jaLDbTnKhw8GyzpmadA6lJscj0rJOVIhYoyI=~4338488~3486788'
    }
    proxies = get_proxy()
    response = request_with_retry("POST", url, headers=headers, data=payload, proxies= proxies)

    return response.json()
