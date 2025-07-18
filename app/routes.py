from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import StoreRequest, StoreResponse
from app.scraper.shopify_scraper import extract_insights, get_competitor_insights
from app.database import save_store_response

insights_router = APIRouter()

@insights_router.post("/fetch_insights", response_model=StoreResponse)
def fetch_insights(request: StoreRequest):
    try:
        data = extract_insights(request.website_url)
        if not data:
            raise HTTPException(status_code=401, detail="Invalid or non-Shopify store URL")
        save_store_response(data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@insights_router.post("/fetch_competitor_insights")
def fetch_competitors(competitor_urls: List[str]):
    try:
        results = get_competitor_insights(competitor_urls)
        return {"competitor_insights": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
