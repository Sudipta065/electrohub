"""Simple checkout business logic.

The demonstration uses one inventory record per product. All checkout changes
are committed together at the end of the function.
"""
from uuid import uuid4

from ..extensions import db
from ..models import Inventory, Order, OrderItem, Payment
from .cart_service import CartError, get_or_create_cart


def checkout(user_id: int, address: str, payment_method: str) -> Order:
    """Convert a valid cart into an order and reduce product stock."""
    if len(address.strip()) < 10:
        raise CartError("Please provide a complete delivery address.")

    allowed_methods = {"CARD_DEMO", "PAY_ON_DELIVERY"}
    if payment_method not in allowed_methods:
        raise CartError("Invalid payment method.")

    cart = get_or_create_cart(user_id)
    if not cart.items:
        raise CartError("Your cart is empty.")

    # Check stock before creating any order records.
    for item in cart.items:
        if item.quantity > item.product.stock:
            raise CartError(f"Insufficient stock for {item.product.name}.")

    order = Order(
        user_id=user_id,
        total_amount=cart.total,
        delivery_address=address.strip(),
        status="CONFIRMED",
    )
    db.session.add(order)

    # Copy cart items to the order and reduce inventory.
    for item in list(cart.items):
        inventory = Inventory.query.filter_by(product_id=item.product_id).first()
        inventory.quantity -= item.quantity

        db.session.add(OrderItem(
            order=order,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
        ))
        db.session.delete(item)

    payment = Payment(
        order=order,
        amount=order.total_amount,
        payment_method=payment_method,
        transaction_id=f"DEMO-{uuid4().hex[:12].upper()}",
        status="PAID" if payment_method == "CARD_DEMO" else "PENDING",
    )
    db.session.add(payment)
    db.session.commit()
    return order

