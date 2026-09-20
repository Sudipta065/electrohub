from datetime import datetime, timezone
from decimal import Decimal

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30))
    role = db.Column(db.String(20), nullable=False, default="CUSTOMER")
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)
    carts = db.relationship("Cart", back_populates="user", cascade="all, delete-orphan")
    orders = db.relationship("Order", back_populates="user")

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "ADMIN"


class Category(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    products = db.relationship("Product", back_populates="category")


class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    category = db.relationship("Category", back_populates="products")
    inventories = db.relationship("Inventory", back_populates="product", cascade="all, delete-orphan")

    @property
    def stock(self):
        return sum(item.quantity for item in self.inventories)


class Store(db.Model):
    __tablename__ = "stores"
    store_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(30))
    inventories = db.relationship("Inventory", back_populates="store", cascade="all, delete-orphan")


class Inventory(db.Model):
    __tablename__ = "inventory"
    inventory_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.store_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    product = db.relationship("Product", back_populates="inventories")
    store = db.relationship("Store", back_populates="inventories")
    __table_args__ = (db.UniqueConstraint("product_id", "store_id"),)


class Cart(db.Model):
    __tablename__ = "carts"
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    user = db.relationship("User", back_populates="carts")
    items = db.relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    @property
    def total(self):
        return sum((item.subtotal for item in self.items), Decimal("0.00"))


class CartItem(db.Model):
    __tablename__ = "cart_items"
    cart_item_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.cart_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    cart = db.relationship("Cart", back_populates="items")
    product = db.relationship("Product")
    __table_args__ = (db.UniqueConstraint("cart_id", "product_id"),)

    @property
    def subtotal(self):
        return self.unit_price * self.quantity


class Order(db.Model):
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    order_date = db.Column(db.DateTime(timezone=True), default=utcnow)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="PENDING")
    delivery_address = db.Column(db.Text, nullable=False)
    user = db.relationship("User", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = db.relationship("Payment", back_populates="order", uselist=False)


class OrderItem(db.Model):
    __tablename__ = "order_items"
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product")

    @property
    def subtotal(self):
        return self.unit_price * self.quantity


class Payment(db.Model):
    __tablename__ = "payments"
    payment_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False, unique=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(200))
    status = db.Column(db.String(20), nullable=False, default="PENDING")
    payment_date = db.Column(db.DateTime(timezone=True), default=utcnow)
    order = db.relationship("Order", back_populates="payment")

