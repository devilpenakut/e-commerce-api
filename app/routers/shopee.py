from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.scrapDetail import getDetailProduct
from ..services.scrapListproduct import getListProductByKeyword,getShopDetail,getLisProductByShop
from ..services.scrapCategory import getAllCategory

router = APIRouter()

class DetailProductRequest(BaseModel):
    URL: str = "https://shopee.co.id/familyDr-UA-Asam-Urat-Strip-25-Tes-i.408323563.8034170963"

class ScrapByKeywordRequest(BaseModel):
    keyword: str = "baju couple"
    page: int = 1
    filter: str = "terbaru  "
    
class ScrapShopDetailRequest(BaseModel):
    shop_username: str = "shastore08"

class ScrapByShopRequest(BaseModel):
    shopID: str = "613038935"

@router.post("/detailProduct")
async def scrape_detail_product(data: DetailProductRequest):
    try:
        result = getDetailProduct(data.URL)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scrapByKeyword")
async def scrape_products_by_keyword(data: ScrapByKeywordRequest):
    try:
        result = getListProductByKeyword(data.keyword, data.page, data.filter)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/shopDetailShop")
async def scrape_shop_detail(data: ScrapShopDetailRequest):
    try:
        result = getShopDetail(data.shop_username)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/scrapByShop")
async def scrape_products_by_shop(data: ScrapByShopRequest):
    try:
        result = getLisProductByShop(data.shopID)
        return {"items": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/allCategory")
async def get_all_category():
    try:
        result = getAllCategory()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))