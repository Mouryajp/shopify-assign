## Shopify Store Insights Fetcher   
This is a Python-based FastAPI backend application that extracts structured insights from any given **Shopify-powered store**, without using the official Shopify API.

## Features
Extracts:
-Full Product Catalog (`/products.json`)
-Hero Products from homepage
-Privacy Policy, Return/Refund Policy
-Brand FAQs (even if structured irregularly)
-Social Media handles (Instagram, FB, TikTok)
-Contact Details (Emails, Phone Numbers)
-About Brand section
-Important links (Track Order, Blog, Contact Us)

RESTful API: `POST /fetch_insights`
Clean architecture: Pydantic models, SOLID principles, modular code
Proper error handling with HTTP status codes

### Bonus
`POST /fetch_competitor_insights`: Dynamically pass multiple Shopify URLs and fetch structured insights
All brand/product data is stored in a SQLite DB (`shopify.db`) on startup

## Project Structure

shopify_assign/
├── app/
│ ├── main.py # FastAPI entrypoint
│ ├── routes.py # API endpoints
│ ├── schemas.py # Pydantic models
│ ├── scraper/
│ │ └── shopify_scraper.py # Core scraping logic
│ └── database.py # SQLite DB persistence
├──requirements.txt


## How to Run

### 1. Install dependencies

 pip install -r requirements.txt

### 2. Start the server

uvicorn app.main:app --reload

### 2. Start the server

 Visit: http://127.0.0.1:8000/docs


## Sample Usage
### /fetch_insights
POST /fetch_insights
{
  "website_url": "https://memy.co.in"
}
### /fetch_competitor_insights
POST /fetch_competitor_insights
[
  "https://hairoriginals.com",
  "https://www.fashionnova.com/"
]


