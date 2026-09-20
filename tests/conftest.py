import pytest

from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models import Category, Inventory, Product, Store, User


@pytest.fixture()
def app():
    application = create_app(TestConfig)
    with application.app_context():
        db.create_all()
        category = Category(name="Laptops")
        store = Store(name="Test Store", address="1 Test Street, Sydney NSW")
        product = Product(category=category, sku="TEST-001", name="Test Laptop",
                          brand="TestBrand", description="Test product", price=999)
        db.session.add_all([category, store, product])
        db.session.flush()
        db.session.add(Inventory(product=product, store=store, quantity=5))
        admin = User(first_name="Admin", last_name="User", email="admin@test.com", role="ADMIN")
        admin.set_password("Password123!")
        db.session.add(admin)
        db.session.commit()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register(client, email="customer@test.com"):
    return client.post("/auth/register", data={"first_name": "Test", "last_name": "Customer",
        "email": email, "password": "Password123!"}, follow_redirects=True)

