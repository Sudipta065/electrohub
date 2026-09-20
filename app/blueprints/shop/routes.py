from flask import Blueprint, abort, render_template, request
from sqlalchemy import or_

from ...extensions import db
from ...models import Category, Product

bp = Blueprint("shop", __name__)


@bp.get("/")
def home():
    products = Product.query.order_by(Product.created_at.desc()).limit(4).all()
    return render_template("shop/home.html", products=products)


@bp.get("/products")
def catalog():
    query = Product.query
    search = request.args.get("q", "").strip()
    category_id = request.args.get("category", type=int)
    if search:
        term = f"%{search}%"
        query = query.filter(or_(Product.name.ilike(term), Product.brand.ilike(term), Product.sku.ilike(term)))
    if category_id:
        query = query.filter_by(category_id=category_id)
    products = query.order_by(Product.name).all()
    categories = Category.query.order_by(Category.name).all()
    return render_template("shop/catalog.html", products=products, categories=categories,
                           search=search, selected_category=category_id)


@bp.get("/products/<int:product_id>")
def product_detail(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        abort(404)
    return render_template("shop/product_detail.html", product=product)

