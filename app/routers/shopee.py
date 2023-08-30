from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.scrapDetail import getDetailProduct
from ..services.scrapListproduct import getListProductByKeyword,getShopDetail,getLisProductByShop
from ..services.scrapCategory import getAllCategory , getAllCategoryLevel3
import redis
import json
from functools import wraps


router = APIRouter()

redis_host = "redis"  # This matches the service name in docker-compose.yml
redis_port = 6379
redis_password = ""
redis_db = 0

redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)

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

class DetailProductRequest(BaseModel):
    URL: str = "https://shopee.co.id/familyDr-UA-Asam-Urat-Strip-25-Tes-i.408323563.8034170963"

class ScrapByKeywordRequest(BaseModel):
    keyword: str = "baju couple"
    page: int = 1
    # filter: str = "terbaru"
    
class ScrapShopDetailRequest(BaseModel):
    shop_username: str = "shastore08"

class ScrapByShopRequest(BaseModel):
    shopID: str = "613038935"
    
class ScrapCategoryLevel3Request(BaseModel):
    level2ID: str = "11044352"

@router.post("/detailProduct")
@cache_response(redis_client, "detail_product")
async def scrape_detail_product(data: DetailProductRequest):
    try:
        result = getDetailProduct(data.URL)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scrapByKeyword")
@cache_response(redis_client, "scrap_by_keyword")
async def scrape_products_by_keyword(data: ScrapByKeywordRequest):
    try:
        result = getListProductByKeyword(data.keyword, data.page)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/shopDetailShop")
@cache_response(redis_client, "shop_detail_shop")
async def scrape_shop_detail(data: ScrapShopDetailRequest):
    try:
        result = getShopDetail(data.shop_username)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/scrapByShop")
@cache_response(redis_client, "scrap_by_shop")
async def scrape_products_by_shop(data: ScrapByShopRequest):
    try:
        result = getLisProductByShop(data.shopID)
        return {"items": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/allCategory")
@cache_response(redis_client, "all_category")
async def get_all_category():
    try:
        result = getAllCategory()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/allCategoryLevel3")
@cache_response(redis_client, "all_category_level3")
async def get_all_category_level3(data: ScrapCategoryLevel3Request):
    try:
        result = getAllCategoryLevel3(data.level2ID)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    