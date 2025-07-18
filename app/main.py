from fastapi import FastAPI, HTTPException
from app.routes import insights_router
from app.database import create_tables

app = FastAPI(title="Shopify Store Insights Fetcher")

app.include_router(insights_router, prefix="")

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
def root():
    return {"message": "Welcome to the Shopify Insights Fetcher API"}