from fastapi import FastAPI
from app.routes import insights_router

app = FastAPI(title="Shopify Store Insights Fetcher")

@app.get("/")
def root():
    return {"message": "Welcome to the Shopify Insights Fetcher API"}

app.include_router(insights_router, prefix="")
