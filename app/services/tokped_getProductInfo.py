from .http_utils import request_with_retry
import random
import string
import re
import os
import json
import urllib.parse


def randomPort():
    # random antara 10000 - 10004 ubah ke string
    return str(random.randint(10000, 10004))

def getRating(productID):
  url = "https://gql.tokopedia.com/graphql/productRatingAndTopics"

  payload = json.dumps([
    {
      "operationName": "productRatingAndTopics",
      "variables": {
        "productID": productID
      },
      "query": "query productRatingAndTopics($productID: String!) {\n  productrevGetProductRatingAndTopics(productID: $productID) {\n    productID\n    rating {\n      positivePercentageFmt\n      ratingScore\n      totalRating\n      totalRatingWithImage\n      totalRatingTextAndImage\n      detail {\n        rate\n        totalReviews\n        formattedTotalReviews\n        percentageFloat\n        __typename\n      }\n      __typename\n    }\n    topics {\n      rating\n      ratingFmt\n      formatted\n      key\n      reviewCount\n      reviewCountFmt\n      show\n      __typename\n    }\n    availableFilters {\n      withAttachment\n      rating\n      topics\n      helpfulness\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
  ])
  headers = {
    'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'X-Version': '2d6fd72',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'Referer': 'https://www.tokopedia.com/johnsonnjohnson/johnson-s-gift-box-paket-hadiah-bayi?src=topads',
    'X-Source': 'tokopedia-lite',
    'X-Tkpd-Lite-Service': 'zeus',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': '_abck=3FE435785D7678DE932851525032B412~-1~YAAQJr4vF2SBuwuMAQAATUjsGQod3D3zepA7vHQcfHbrvDmGTqjBAzcRX5kp1QHWuVTnU1Zg3uN3zTYpBvK69qtSPLdNh1FRvXavdZeF4jYyYTfctUn5O+YupALe5oEavlDx0+5n8w+AQdw6Gd75X1V3HPneodzCEwWde64HFE63+CnUPBLUMipc+4eu8Izf3/fGT7luA5X5aY3V0Safa688gzN/psjSPvjx86OGtOSVcxx5c2WxgW0JW2BHCKmCHIGVGO0130tQiq7eWiI6IzjzlJbf2jXfZ0XMwMHYMAEgyeO7P6OJJylJYAnm474yZUu51UKUsde6i52WF4FqQ52Z0HV6jDhnl6bRj6npfK0maKlP04dv2tHfXs/ypu764Wkd1yBmVxnbXYLYbA==~-1~-1~-1; bm_sz=3A79C38DE771EFC34B5562DEAA3708F2~YAAQJr4vF2WBuwuMAQAATUjsGRXd+9Z4ONVLjZonnNcPR7aS4EXstfUz2MG5XvnJAiJp9rd3ZPtQmjcZnjXRJ6BkjzIAEqAvI6TU0r1rCtyZApsfdlM4/qyhJ/HZSyPZiiAr16y19V4c0nvCbsx1XrA9Ep0nQSGZ7aq1Y2dRFoIBppxapATp0HPKZvyl0xvptQW1vAJXsjbrcSBKy1lpbUIheNmGhxMr9Z+zE5x+o/Jl1cyezqTyelZ2imiSyD/qlFUn8Ag/il5TtZxM8O2oDokdM4VVvQoRntTUjnFkJ217l4geR+w=~3683889~3289654'
  }

  proxy_url = (
        "http://firhandarief;country=ID:57fee1-d01161-63d5f9-beed9f-8105b3@38.84.70.226:"
        + randomPort()
    )
  proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
  response = request_with_retry("POST", url, headers=headers, data=payload, proxies= proxies)
  response = response.json()
  response = response[0]['data']['productrevGetProductRatingAndTopics']
  return response


def getProductInfo(productURL):
  pattern = r"tokopedia\.com\/([^\/]+)\/([^?]+)"
  match = re.search(pattern, productURL)
    
  
  shopUsername = match.group(1)
  title_slug = match.group(2)
    
  url = "https://gql.tokopedia.com/graphql/PDPGetLayoutQuery"

  payload = json.dumps([
    {
      "operationName": "PDPGetLayoutQuery",
      "variables": {
        "shopDomain": shopUsername,
        "productKey": title_slug,
        "layoutID": "",
        "apiVersion": 1,
        "tokonow": {
          "shopID": "11530573",
          "whID": "12210375",
          "serviceType": "2h"
        },
        "userLocation": {
          "cityID": "176",
          "addressID": "0",
          "districtID": "2274",
          "postalCode": "",
          "latlon": ""
        },
        "extParam": "src%3Dshop%26whid%3D1573699"
      },
      "query": "fragment ProductVariant on pdpDataProductVariant {\n  errorCode\n  parentID\n  defaultChild\n  sizeChart\n  totalStockFmt\n  variants {\n    productVariantID\n    variantID\n    name\n    identifier\n    option {\n      picture {\n        urlOriginal: url\n        urlThumbnail: url100\n        __typename\n      }\n      productVariantOptionID\n      variantUnitValueID\n      value\n      hex\n      stock\n      __typename\n    }\n    __typename\n  }\n  children {\n    productID\n    price\n    priceFmt\n    optionID\n    optionName\n    productName\n    productURL\n    picture {\n      urlOriginal: url\n      urlThumbnail: url100\n      __typename\n    }\n    stock {\n      stock\n      isBuyable\n      stockWordingHTML\n      minimumOrder\n      maximumOrder\n      __typename\n    }\n    isCOD\n    isWishlist\n    campaignInfo {\n      campaignID\n      campaignType\n      campaignTypeName\n      campaignIdentifier\n      background\n      discountPercentage\n      originalPrice\n      discountPrice\n      stock\n      stockSoldPercentage\n      startDate\n      endDate\n      endDateUnix\n      appLinks\n      isAppsOnly\n      isActive\n      hideGimmick\n      isCheckImei\n      minOrder\n      __typename\n    }\n    thematicCampaign {\n      additionalInfo\n      background\n      campaignName\n      icon\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ProductMedia on pdpDataProductMedia {\n  media {\n    type\n    urlOriginal: URLOriginal\n    urlThumbnail: URLThumbnail\n    urlMaxRes: URLMaxRes\n    videoUrl: videoURLAndroid\n    prefix\n    suffix\n    description\n    variantOptionID\n    __typename\n  }\n  videos {\n    source\n    url\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCategoryCarousel on pdpDataCategoryCarousel {\n  linkText\n  titleCarousel\n  applink\n  list {\n    categoryID\n    icon\n    title\n    isApplink\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductHighlight on pdpDataProductContent {\n  name\n  price {\n    value\n    currency\n    __typename\n  }\n  campaign {\n    campaignID\n    campaignType\n    campaignTypeName\n    campaignIdentifier\n    background\n    percentageAmount\n    originalPrice\n    discountedPrice\n    originalStock\n    stock\n    stockSoldPercentage\n    threshold\n    startDate\n    endDate\n    endDateUnix\n    appLinks\n    isAppsOnly\n    isActive\n    hideGimmick\n    __typename\n  }\n  thematicCampaign {\n    additionalInfo\n    background\n    campaignName\n    icon\n    __typename\n  }\n  stock {\n    useStock\n    value\n    stockWording\n    __typename\n  }\n  variant {\n    isVariant\n    parentID\n    __typename\n  }\n  wholesale {\n    minQty\n    price {\n      value\n      currency\n      __typename\n    }\n    __typename\n  }\n  isCashback {\n    percentage\n    __typename\n  }\n  isTradeIn\n  isOS\n  isPowerMerchant\n  isWishlist\n  isCOD\n  preorder {\n    duration\n    timeUnit\n    isActive\n    preorderInDays\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCustomInfo on pdpDataCustomInfo {\n  icon\n  title\n  isApplink\n  applink\n  separator\n  description\n  __typename\n}\n\nfragment ProductInfo on pdpDataProductInfo {\n  row\n  content {\n    title\n    subtitle\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDetail on pdpDataProductDetail {\n  content {\n    title\n    subtitle\n    applink\n    showAtFront\n    isAnnotation\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDataInfo on pdpDataInfo {\n  icon\n  title\n  isApplink\n  applink\n  content {\n    icon\n    text\n    __typename\n  }\n  __typename\n}\n\nfragment ProductSocial on pdpDataSocialProof {\n  row\n  content {\n    icon\n    title\n    subtitle\n    applink\n    type\n    rating\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDetailMediaComponent on pdpDataProductDetailMediaComponent {\n  title\n  description\n  contentMedia {\n    url\n    ratio\n    type\n    __typename\n  }\n  show\n  ctaText\n  __typename\n}\n\nquery PDPGetLayoutQuery($shopDomain: String, $productKey: String, $layoutID: String, $apiVersion: Float, $userLocation: pdpUserLocation, $extParam: String, $tokonow: pdpTokoNow) {\n  pdpGetLayout(shopDomain: $shopDomain, productKey: $productKey, layoutID: $layoutID, apiVersion: $apiVersion, userLocation: $userLocation, extParam: $extParam, tokonow: $tokonow) {\n    requestID\n    name\n    pdpSession\n    basicInfo {\n      alias\n      createdAt\n      isQA\n      id: productID\n      shopID\n      shopName\n      minOrder\n      maxOrder\n      weight\n      weightUnit\n      condition\n      status\n      url\n      needPrescription\n      catalogID\n      isLeasing\n      isBlacklisted\n      isTokoNow\n      menu {\n        id\n        name\n        url\n        __typename\n      }\n      category {\n        id\n        name\n        title\n        breadcrumbURL\n        isAdult\n        isKyc\n        minAge\n        detail {\n          id\n          name\n          breadcrumbURL\n          isAdult\n          __typename\n        }\n        __typename\n      }\n      txStats {\n        transactionSuccess\n        transactionReject\n        countSold\n        paymentVerified\n        itemSoldFmt\n        __typename\n      }\n      stats {\n        countView\n        countReview\n        countTalk\n        rating\n        __typename\n      }\n      __typename\n    }\n    components {\n      name\n      type\n      position\n      data {\n        ...ProductMedia\n        ...ProductHighlight\n        ...ProductInfo\n        ...ProductDetail\n        ...ProductSocial\n        ...ProductDataInfo\n        ...ProductCustomInfo\n        ...ProductVariant\n        ...ProductCategoryCarousel\n        ...ProductDetailMediaComponent\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
  ])
  headers = {
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'X-Version': '8ab2593',
    'X-TKPD-AKAMAI': 'pdpGetLayout',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'Referer': 'https://www.tokopedia.com/',
    'X-Source': 'tokopedia-lite',
    'x-device': 'desktop',
    'X-Tkpd-Lite-Service': 'zeus',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': '_abck=7053B61DF033355E32F25D33E634A7DA~-1~YAAQBNs4fayyYNmKAQAALdT86Aq+xqQD7/dXZ6vdKoKennZLgyykSXWF2t7jBbpRDv5rXx+0vW5+eyMG/15m6CrldKMLebD7uIT4zDFACtrgfc4SLDWAR12cl70XQ0Gc9w373pxdrzF90tE3YwYoYi5tbKrQAt1yvrv4TebcVSuw1anTjI/j3ppqyHsaOxQQ7RkB2fz3NdR07nQfFxY3y0sctRIXdmi8nH4abbH02X4/BqOTi7R61aC1/veIStuwtTvNfiIY6z2V8vWC1zVg3+bwD/7VAxLPuJC7jGAemXvbxJXIRqC98y0Nsf7wwcyT1t0HEgoiiDBkLtIuxolK57b2/GKQvy2OpYvdGOGK8Uc6GW5bTfaTGC+dmUyFBQJeSjkDlLPIvzlnVQ4y5Q==~-1~-1~-1; bm_sz=8073B4857B14B0CF0EAB4BACC07A6774~YAAQBNs4fa2yYNmKAQAALdT86BUt9Tu2MyzoHa7BC2mnf8sk1rlykIWyN7wHs4MJtrn0WIwEvaGZWunnAE3MkAEXvLA/yZvH0v9bPN1VUbLuWJMnKT5ofGRlLltMspOY68bdkBVNBol5lkfjvVEXRsfhmv0qMx6OhJ120UA3YIyXqOUCL9mFQRoGZrZrT5hYFe6Jc3HtzMu2o041scZYNdAc8uDnFzJDhwFzHo+b7MnTTad6s2QHNcxZRIZOnFcPjivcU/Xd4RmqENz2eAQqeU8gOKZMbtigDhxA4ctOm7gGkHvtNww=~3421490~4535604'
  }

  proxy_url = (
        "http://firhandarief;country=ID:57fee1-d01161-63d5f9-beed9f-8105b3@38.84.70.226:"
        + randomPort()
    )
  proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
  response = request_with_retry("POST", url, headers=headers, data=payload, proxies= proxies)

  productID = response.json()[0]['data']['pdpGetLayout']['basicInfo']['id']
  data_rating = getRating(productID)
  new_response = response.json()
  new_response[0]['data']['rating'] = data_rating
  # print(new_response[0]['data']['rating'])
  # print(new_response)
  return new_response