from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Optional

class Product(BaseModel):
    title: str
    price: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

class StoreRequest(BaseModel):
    website_url: HttpUrl

class StoreResponse(BaseModel):
    brand_name: Optional[str]
    hero_products: List[Product] = []
    product_catalog: List[Product] = []
    policies: Dict[str, Optional[str]] = {}
    faqs: List[Dict[str, str]] = []
    social_links: Dict[str, str] = {}
    contact_details: Dict[str, List[str]] = {}
    brand_about: Optional[str] = None
    important_links: Dict[str, str] = {}
