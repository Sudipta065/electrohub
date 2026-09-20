import os
from decimal import Decimal

from .extensions import db
from .models import Category, Inventory, Product, Store, User


PRODUCTS = [
    ("Laptops", "Computers for work, study and entertainment", "LAP-001", "Aspire 15 Laptop", "Acer", "15.6-inch everyday laptop with fast SSD storage.", "899.00", "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80"),
    ("Phones", "Smartphones and accessories", "PHN-001", "Galaxy A Series", "Samsung", "5G smartphone with a vivid display and long battery life.", "649.00", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80"),
    ("TVs", "Televisions and home cinema", "TV-001", "55-inch 4K Smart TV", "LG", "4K UHD smart television with streaming applications.", "1199.00", "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&w=900&q=80"),
    ("Audio", "Headphones, speakers and audio", "AUD-001", "Noise Cancelling Headphones", "Sony", "Wireless over-ear headphones with active noise cancellation.", "399.00", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80"),
    ("Gaming", "Consoles and gaming accessories", "GAM-001", "Wireless Gaming Controller", "Microsoft", "Ergonomic controller for console and PC gaming.", "89.00", "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?auto=format&fit=crop&w=900&q=80"),
    ("Cameras", "Digital cameras and accessories", "CAM-001", "Mirrorless Camera", "Canon", "Compact mirrorless camera for high-quality photos and video.", "1399.00", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=80"),
]


def seed_database():
    if not Store.query.first():
        db.session.add(Store(name="Sydney Central", address="Sydney NSW 2000", phone="02 9000 0000"))
    db.session.flush()
    store = Store.query.first()

    for category_name, category_description, sku, name, brand, description, price, image in PRODUCTS:
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name, description=category_description)
            db.session.add(category)
            db.session.flush()
        product = Product.query.filter_by(sku=sku).first()
        if not product:
            product = Product(category=category, sku=sku, name=name, brand=brand,
                              description=description, price=Decimal(price), image_url=image)
            db.session.add(product)
            db.session.flush()
            db.session.add(Inventory(product=product, store=store, quantity=10))

    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com").lower()
    if not User.query.filter_by(email=admin_email).first():
        admin = User(first_name="Store", last_name="Admin", email=admin_email, role="ADMIN")
        admin.set_password(os.getenv("ADMIN_PASSWORD", "ChangeMe123!"))
        db.session.add(admin)
    db.session.commit()

