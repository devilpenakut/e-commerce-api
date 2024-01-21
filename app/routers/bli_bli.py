from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import redis
import json
from functools import wraps

from ..services.blibli_getCategories import getLevel1,getLevel2
from ..services.blibli_getListProductByCat import getLisProductByCat
from ..services.blibli_getListProductByKeyword import getListProductByKey
from ..services.blibli_getListSeller import getListSeller
from ..services.blibli_getDetailProduct import getDetailProduct
from ..services.blibli_getInfoShop import getInfoShop
from ..services.blibli_getListProductByShop import getListProductByShop

router = APIRouter()

redis_host = "redis"  # This matches the service name in docker-compose.yml
redis_port = 6379
redis_password = ""
redis_db = 0

redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)


class getLevel2Request(BaseModel):
    level1_id: str = "68cc95aa-78b3-4db9-9235-24746ee3abf8"

class getListProductByCatRequest(BaseModel):
    category_code: str = "PE-1000017"
    page: int = 1

class getListProductByKeywordRequest(BaseModel):
    category_code: str = "Baju Anak"
    page: int = 1
    
class getListSellerRequest(BaseModel):
    keyword_seller: str = "baju"
    page: int = 1
    
class getDetailProductRequest(BaseModel):
    URL : str = 'https://www.blibli.com/p/setelan-baju-anak-laki-laki-harian-robotic-0-8-tahun/ps--PRA-70043-00162?ds=PRA-70043-00162-00001&source=SEARCH&sid=85ee790ceaabfe94&cnc=false&pickupPointCode=PP-3189251&pid1=PRA-70043-00162&tag=trending'
    
class getInfoShopRequest(BaseModel):
    namaToko: str = "Blibli - Apple Authorised Reseller"

class getListProductByShopRequest(BaseModel):
    namaToko: str = "Blibli - Apple Authorised Reseller"
    page: int = 1

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

@router.get("/getCategoryLevel1", tags=["BliBli"])
@cache_response(redis_client, "getCategoryLevel1")
async def getCategoryLevel1():
    try:
        result = getLevel1()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/getCategoryChildren", tags=["BliBli"])
@cache_response(redis_client, "getCategoryChildren")
async def getCategoryLevel2(request: getLevel2Request):
    try:
        result = getLevel2(request.level1_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/getListProductByCat", tags=["BliBli"])
@cache_response(redis_client, "getListProductByCat")
async def getListProductByCat(request: getListProductByCatRequest):
    try:
        result = getLisProductByCat(request.category_code, request.page)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/getListProductByKeyword", tags=["BliBli"])
@cache_response(redis_client, "getListProductByKeyword")
async def getListProductByKeyword(request: getListProductByKeywordRequest):
    try:
        result = getListProductByKey(request.category_code, request.page)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/getListSeller", tags=["BliBli"])
@cache_response(redis_client, "getListSeller")
async def getListSellerKeyword(request: getListSellerRequest):
    try:
        result = getListSeller(request.keyword_seller, request.page)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/getDetailProduct", tags=["BliBli"])
@cache_response(redis_client, "getDetailProduct")
async def getDetailProductBySku(request: getDetailProductRequest):
    try:
        result = getDetailProduct(request.URL)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/getInfoShop", tags=["BliBli"])
@cache_response(redis_client, "getInfoShop")
async def getInfoShopP(request: getInfoShopRequest):
    try:
        result = getInfoShop(request.namaToko)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/getListProductByShop", tags=["BliBli"])
@cache_response(redis_client, "getListProductByShop")
async def getListProductByShopP(request: getListProductByShopRequest):
    try:
        result = getListProductByShop(request.namaToko, request.page)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))