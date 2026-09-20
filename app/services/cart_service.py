from ..extensions import db
from ..models import Cart, CartItem, Product


class CartError(ValueError):
    pass


def get_or_create_cart(user_id: int) -> Cart:
    """Return the user's cart, creating it when necessary."""
    cart = Cart.query.filter_by(user_id=user_id).order_by(Cart.cart_id.desc()).first()
    if cart is None:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    return cart


def add_product(user_id: int, product_id: int, quantity: int = 1) -> Cart:
    """Add a product after checking quantity and available stock."""
    if quantity < 1:
        raise CartError("Quantity must be at least one.")
    product = db.session.get(Product, product_id)
    if not product:
        raise CartError("Product not found.")
    cart = get_or_create_cart(user_id)
    item = CartItem.query.filter_by(cart_id=cart.cart_id, product_id=product_id).first()
    requested = quantity + (item.quantity if item else 0)
    if requested > product.stock:
        raise CartError(f"Only {product.stock} item(s) are available.")
    if item:
        item.quantity = requested
    else:
        db.session.add(CartItem(cart=cart, product=product, quantity=quantity,
                                unit_price=product.price))
    db.session.commit()
    return cart


def update_item(user_id: int, item_id: int, quantity: int) -> Cart:
    """Change an item quantity; zero removes it from the cart."""
    cart = get_or_create_cart(user_id)
    item = CartItem.query.filter_by(cart_id=cart.cart_id, cart_item_id=item_id).first()
    if not item:
        raise CartError("Cart item not found.")
    if quantity <= 0:
        db.session.delete(item)
    elif quantity > item.product.stock:
        raise CartError(f"Only {item.product.stock} item(s) are available.")
    else:
        item.quantity = quantity
    db.session.commit()
    return cart
