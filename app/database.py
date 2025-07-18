import sqlite3
from app.schemas import StoreResponse, Product

def create_tables():
    with sqlite3.connect("shopify.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_name TEXT,
                brand_about TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_id INTEGER,
                title TEXT,
                price TEXT,
                description TEXT,
                image TEXT,
                FOREIGN KEY (store_id) REFERENCES stores(id)
            )
        """)
        conn.commit()

def save_store_response(data: StoreResponse):
    with sqlite3.connect("shopify.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO stores (brand_name, brand_about) VALUES (?, ?)",
                       (data.brand_name, data.brand_about))
        store_id = cursor.lastrowid
        for product in data.product_catalog:
            cursor.execute("""
                INSERT INTO products (store_id, title, price, description, image)
                VALUES (?, ?, ?, ?, ?)""",
                (store_id, product.title, product.price, product.description, product.image))
        conn.commit()