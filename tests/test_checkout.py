from app.models import Inventory, Order
from .conftest import register


def test_customer_can_add_to_cart_and_checkout(app, client):
    register(client)
    response = client.post("/account/cart/add/1", data={"quantity": 2}, follow_redirects=True)
    assert b"Product added" in response.data
    response = client.post("/account/checkout", data={
        "address": "100 George Street, Sydney NSW 2000", "payment_method": "CARD_DEMO"
    }, follow_redirects=True)
    assert b"placed successfully" in response.data
    with app.app_context():
        assert Order.query.count() == 1
        assert Inventory.query.first().quantity == 3


def test_checkout_rejects_empty_cart(client):
    register(client)
    response = client.post("/account/checkout", data={
        "address": "100 George Street, Sydney NSW 2000", "payment_method": "CARD_DEMO"
    }, follow_redirects=True)
    assert b"cart is empty" in response.data


def test_admin_page_rejects_customer(client):
    register(client)
    assert client.get("/admin/").status_code == 403

