import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from app.schemas import StoreResponse, Product
import re

def fetch_page(url):
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return None
    return BeautifulSoup(response.text, 'html.parser')

def get_json_products(base_url):
    try:
        res = requests.get(urljoin(str(base_url), "/products.json"))
        return res.json().get("products", [])
    except:
        return []

def extract_emails_phones(text):
    emails = re.findall(r"[\w\.-]+@[\w\.-]+", text)
    phones = re.findall(r"\+?\d[\d\s\-()]{7,}\d", text)
    return emails, phones

def extract_insights(website_url: str) -> StoreResponse:
    website_url = str(website_url).strip().rstrip('/')
    soup = fetch_page(website_url)
    if not soup:
        return None

    text = soup.get_text()
    emails, phones = extract_emails_phones(text)

    pages = {
        "privacy_policy": "/pages/privacy-policy",
        "return_policy": "/pages/return-policy",
        "about_us": "/pages/about-us",
        "faqs": "/pages/faqs"
    }
    policies = {}
    about = ""
    faqs = []
    for name, route in pages.items():
        sub_page = fetch_page(urljoin(website_url, route))
        if sub_page:
            content = sub_page.get_text(strip=True)
            if name == "about_us":
                about = content
            elif name == "faqs":
                faqs = parse_faqs(sub_page)
            else:
                policies[name] = content

    hero_products = []
    for img_tag in soup.select("img")[:5]:
        hero_products.append(Product(title="Hero Product", image=img_tag.get("src")))

    raw_products = get_json_products(website_url)
    catalog = [
        Product(
            title=prod.get("title"),
            price=str(prod.get("variants", [{}])[0].get("price")),
            description=prod.get("body_html"),
            image=prod.get("image", {}).get("src")
        )
        for prod in raw_products
    ]

    social_links = {}
    for link in soup.find_all("a", href=True):
        href = link['href']
        if "instagram.com" in href:
            social_links["instagram"] = href
        if "facebook.com" in href:
            social_links["facebook"] = href
        if "tiktok.com" in href:
            social_links["tiktok"] = href

    important_links = {}
    for link in soup.find_all("a", href=True):
        if any(kw in link.text.lower() for kw in ["contact", "track", "blog"]):
            important_links[link.text.strip()] = urljoin(website_url, link['href'])

    return StoreResponse(
        brand_name=website_url.split('//')[-1].split('.')[0].capitalize(),
        hero_products=hero_products,
        product_catalog=catalog,
        policies=policies,
        faqs=faqs,
        social_links=social_links,
        contact_details={"emails": emails, "phones": phones},
        brand_about=about,
        important_links=important_links
    )

def parse_faqs(soup):
    faqs = []
    for q in soup.find_all(['h2', 'h3']):
        next_p = q.find_next_sibling('p')
        if next_p:
            faqs.append({"question": q.get_text(), "answer": next_p.get_text()})
    return faqs

def get_competitor_insights(competitor_urls):
    insights = []
    for comp_url in competitor_urls:
        data = extract_insights(comp_url)
        if data:
            insights.append({"url": comp_url, "data": data.dict()})
    return insights
