"""
Database module for product catalog
"""

import sqlite3
import json
from typing import List, Dict
import re

DB_PATH = "commerce.db"

def init_database():
    """Initialize database with product catalog"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            image_url TEXT NOT NULL,
            features TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Check if products exist
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert sample products
        sample_products = get_sample_products()
        for product in sample_products:
            cursor.execute("""
                INSERT INTO products (name, description, category, price, image_url, features)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                product['name'],
                product['description'],
                product['category'],
                product['price'],
                product['image_url'],
                json.dumps(product.get('features', []))
            ))
    
    conn.commit()
    conn.close()

def get_sample_products() -> List[Dict]:
    """Return sample product catalog"""
    return [
        {
            "name": "Nike Pro Sport T-Shirt",
            "description": "Performance t-shirt made from breathable Dri-FIT fabric. Perfect for sports and athletic activities.",
            "category": "Clothing > T-Shirts",
            "price": 29.99,
            "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
            "features": ["Breathable", "Moisture-wicking", "Athletic fit", "Polyester blend"]
        },
        {
            "name": "Adidas Running Shorts",
            "description": "Comfortable running shorts with moisture-wicking fabric and built-in brief. Ideal for jogging and workouts.",
            "category": "Clothing > Shorts",
            "price": 34.99,
            "image_url": "https://teamexpress.com/cdn/shop/files/hs7692_6.jpg?v=1754078361&width=1200",
            "features": ["Lightweight", "Quick-dry", "Pocket included", "Elastic waistband"]
        },
        {
            "name": "Professional Training Shoes",
            "description": "Versatile training shoes for gym workouts and cross-training. Features responsive cushioning.",
            "category": "Footwear > Athletic Shoes",
            "price": 89.99,
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
            "features": ["Cushioned", "Durable", "Non-slip sole", "Breathable"]
        },
        {
            "name": "Gym Gloves with Wrist Support",
            "description": "Weightlifting gloves with padded palms and adjustable wrist straps. Protect your hands during workouts.",
            "category": "Accessories > Gym Equipment",
            "price": 24.99,
            "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=400",
            "features": ["Padded", "Wrist support", "Breathable", "Machine washable"]
        },
        {
            "name": "Yoga Mat - Premium Edition",
            "description": "Extra thick yoga mat with non-slip surface. Perfect for yoga, pilates, and floor exercises.",
            "category": "Accessories > Yoga",
            "price": 39.99,
            "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400",
            "features": ["Non-slip", "Extra thick", "Portable", "Easy to clean"]
        },
        {
            "name": "Protein Shaker Bottle",
            "description": "BPA-free plastic shaker bottle with mixing ball. Perfect for protein shakes and supplements.",
            "category": "Accessories > Supplements",
            "price": 12.99,
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",
            "features": ["BPA-free", "Leak-proof", "Measurement lines", "Dishwasher safe"]
        },
        {
            "name": "Wireless Bluetooth Earbuds",
            "description": "Sweat-proof wireless earbuds with noise cancellation. Perfect for workouts and running.",
            "category": "Electronics > Audio",
            "price": 49.99,
            "image_url": "https://images.unsplash.com/photo-1606225456115-9b4f94c8c4a6?w=400",
            "features": ["Noise cancellation", "Sweat-proof", "8-hour battery", "Bluetooth 5.0"]
        },
        {
            "name": "Premium Sports Watch",
            "description": "Fitness tracker with heart rate monitor, GPS, and 7-day battery life. Tracks steps, calories, and sleep.",
            "category": "Electronics > Wearables",
            "price": 149.99,
            "image_url": "https://images.unsplash.com/photo-1544117519-31a4b719223d?w=400",
            "features": ["Heart rate monitor", "GPS", "Waterproof", "Smart notifications"]
        }
    ]

def get_all_products() -> List[Dict]:
    """Get all products from database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    
    products = []
    for row in rows:
        product = dict(row)
        # Parse features JSON
        if product['features']:
            product['features'] = json.loads(product['features'])
        else:
            product['features'] = []
        products.append(product)
    
    conn.close()
    return products

def search_products_by_text(query: str, products: List[Dict]) -> List[Dict]:
    """Search products by text query using keyword matching"""
    query_lower = query.lower()
    matched = []
    
    for product in products:
        score = 0
        
        # Check name
        if query_lower in product['name'].lower():
            score += 3
        
        # Check description
        if query_lower in product['description'].lower():
            score += 2
        
        # Check category
        if query_lower in product['category'].lower():
            score += 2
        
        # Check features
        for feature in product.get('features', []):
            if query_lower in feature.lower():
                score += 1
        
        # Add keywords matching
        keywords = {
            't-shirt': ['shirt', 'top', 'tshirt'],
            'sports': ['sport', 'athletic', 'athletics', 'training'],
            'shoes': ['shoe', 'sneakers', 'footwear'],
            'shorts': ['short'],
            'gloves': ['glove']
        }
        
        for key, synonyms in keywords.items():
            if key in query_lower:
                for synonym in synonyms:
                    if synonym in product['name'].lower() or synonym in product['description'].lower():
                        score += 2
        
        if score > 0:
            matched.append((score, product))
    
    # Sort by score and return products
    matched.sort(key=lambda x: x[0], reverse=True)
    return [product for _, product in matched]

def search_products_by_image_similarity(image_data: str, products: List[Dict]) -> List[Dict]:
    """
    Simple image search - returns a subset of products from the catalog
    In production, use proper computer vision models to analyze the image
    and match against the catalog
    """
    # For demo purposes, return a small subset of products from the catalog
    # In production, you would use vision models (like CLIP) to extract features
    # from the image and match against product images in the catalog
    
    # Return first 3 products as demo search results
    # In production, this would analyze the image and return only relevant items
    return products[:3]

