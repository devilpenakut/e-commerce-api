from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.scrapDetail import getDetailProduct
from ..services.scrapListproduct import getListProductByKeyword,getShopDetail,getLisProductByShop,getListProductByCat
from ..services.scrapCategory import getAllCategory , getAllCategoryLevel3
from ..services.cookies import addCookies
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

# add clas for array of cookies
class AddShopeeCookies(BaseModel):
    cookies: list = []  
    
# buat class untuk request body catid_lvl1, catid_lvl2, catid_lvl3, page. jika hanya ingin mengambil data dari catid_lvl1, maka catid_lvl2 dan catid_lvl3 tidak perlu diisi
class ScrapByCategoryRequest(BaseModel):
    catid_lvl1: str = ""
    catid_lvl2: str = "11044352"
    catid_lvl3: str = ""
    page: int = 0
    filter_product: str = ""
    location: str = ""

@router.post("/detailProduct", tags=["Shopee"])
# @cache_response(redis_client, "detail_product")
async def scrape_detail_product(data: DetailProductRequest):
    try:
        result = getDetailProduct(data.URL)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scrapByKeyword", tags=["Shopee"])
# @cache_response(redis_client, "scrap_by_keyword")
async def scrape_products_by_keyword(data: ScrapByKeywordRequest):
    try:
        result = getListProductByKeyword(data.keyword, data.page)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/shopDetailShop" , tags=["Shopee"])
# @cache_response(redis_client, "shop_detail_shop")
async def scrape_shop_detail(data: ScrapShopDetailRequest):
    try:
        result = getShopDetail(data.shop_username)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/scrapByShop" , tags=["Shopee"])
# @cache_response(redis_client, "scrap_by_shop")
async def scrape_products_by_shop(data: ScrapByShopRequest):
    try:
        result = getLisProductByShop(data.shopID)
        return {"items": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/allCategory" , tags=["Shopee"])
# @cache_response(redis_client, "all_category")
async def get_all_category():
    try:
        result = getAllCategory()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/allCategoryLevel3" , tags=["Shopee"])
# @cache_response(redis_client, "all_category_level3")
async def get_all_category_level3(data: ScrapCategoryLevel3Request):
    try:
        result = getAllCategoryLevel3(data.level2ID)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/addCookies" , tags=["Shopee"])
async def add_cookies(data: AddShopeeCookies):
    try:
        result = addCookies(data.cookies)
        return {"message": "success add cookies"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/scrapByCategory", description="Mengambil produk berdasarkan kategori.\n\n"
                                              "Pilihan kategori:\n"
                                              "- Jika ingin mengambil level 1, berikan `catid_lvl1`.\n"
                                              "- Jika ingin mengambil level 2, berikan `catid_lvl2`.\n"
                                              "- Jika ingin mengambil level 3 dengan level 2, berikan `catid_lvl2` dan `catid_lvl3`.\n"
                                              "- Jika ingin mengambil level 3 dengan level 1, berikan `catid_lvl1` dan `catid_lvl3`.\n\n"
                                              "Pilihan filter:\n"
                                              "- Jika ingin menggunakan filter, berikan `filter`. Filter yang tersedia: `pop`, `sales`, `ctime`.\n\n"
                                              "Pilihan lokasi:\n"
                                              "- Jika ingin mengambil berdasarkan lokasi, berikan `location`. Contoh: `Jawa Timur`.\n"
, tags=["Shopee"])
                                              
@cache_response(redis_client, "scrap_by_category")    
async def scrape_products_by_category(data: ScrapByCategoryRequest):
    """
    Mengambil produk berdasarkan kategori.

    :param data: Data permintaan yang berisi ID kategori dan nomor halaman.
    :type data: ScrapByCategoryRequest
    :return: Data produk yang diambil.
    """
    try:
        result = getListProductByCat(data.catid_lvl1, data.catid_lvl2, data.catid_lvl3, data.location, data.page, data.filter_product)
        return result
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail=str(e))
