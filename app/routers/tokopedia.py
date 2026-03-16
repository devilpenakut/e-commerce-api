from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import redis
import json
import os
from functools import wraps
from ..services.tokped_getSeller import get_seller
from ..services.tokped_GetAllCategory import getAllCategory
from ..services.tokped_getProductByCat import getProductBycat
from ..services.tokped_getProductByKeyword import getProductByKeyword
from ..services.tokped_getInfoShop import getShopInfo
from ..services.tokped_getProductInfo import getProductInfo
from ..services.tokped_geProductByShop import getProductByShop

router = APIRouter()

redis_client = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379"))

def cache_response(redis_client, redis_key_prefix):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate a unique Redis key based on function name and arguments
            redis_key = f"{redis_key_prefix}:{func.__name__}:{args}:{kwargs}"
            redis_result = redis_client.get(redis_key)

            if redis_result is not None:
                result_dict = json.loads(redis_result)
                return result_dict

            result = await func(*args, **kwargs)

            redis_client.set(redis_key, json.dumps(result))
            return result

        return wrapper
    return decorator

class ScrapListSellerRequest(BaseModel):
    searchSellerList: str = "ichibot"
    page: int = 1
    
class  ScrapListProductRequest(BaseModel):
    page: int = 1
    catId: int = 1889
    
class ScrapListProductByKeywordRequest(BaseModel):
    page: int = 1
    keyword: str = "baju"

class ScrapListInfoShopRequest(BaseModel):
    sellerURL: str = "https://www.tokopedia.com/bajukoki"
    
class ScrapProductInfo(BaseModel):
    productURL: str = "https://www.tokopedia.com/jajanangarut19/cuanki-instan-bandung"
    
class ScrapProductByShop(BaseModel):
    shopId: str = "1973484"
    page: int = 1

@router.post("/seller", tags=["Tokopedia"])
@cache_response(redis_client, "seller")
async def scrap_seller(request: ScrapListSellerRequest):
    try:
        result = get_seller(request.searchSellerList, request.page)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/GetAllCategory", tags=["Tokopedia"])
@cache_response(redis_client, "GetAllCategory")
async def scrap_getAllCategory():
    try:
        result = getAllCategory()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/product", tags=["Tokopedia"])
@cache_response(redis_client, "product")
async def scrap_product(request: ScrapListProductRequest):
    try:
        result = getProductBycat(request.page, request.catId)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/productByKeyword", tags=["Tokopedia"])
@cache_response(redis_client, "productByKeyword")
async def scrap_productByKeyword(request: ScrapListProductByKeywordRequest):
    try:
        result = getProductByKeyword(request.page, request.keyword)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/infoShop", tags=["Tokopedia"])
@cache_response(redis_client, "infoShop")
async def scrap_infoShop(request: ScrapListInfoShopRequest):
    try:
        result = getShopInfo(request.sellerURL)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/productInfo", tags=["Tokopedia"])
@cache_response(redis_client, "productInfo")
async def scrap_productInfo(request: ScrapProductInfo):
    try:
        result = getProductInfo(request.productURL)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/productByShop", tags=["Tokopedia"])
@cache_response(redis_client, "productByShop")
async def scrap_productByShop(request: ScrapProductByShop):
    try:
        result = getProductByShop(request.shopId, request.page)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))