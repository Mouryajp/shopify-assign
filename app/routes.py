from fastapi import APIRouter, HTTPException
from app.schemas import StoreRequest, StoreResponse
from app.scraper.shopify_scraper import extract_insights

insights_router = APIRouter()

@insights_router.post("/fetch_insights", response_model=StoreResponse)
def fetch_insights(request: StoreRequest):
    try:
        data = extract_insights(request.website_url)
        if not data:
            raise HTTPException(status_code=401, detail="Invalid or non-Shopify store URL")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
