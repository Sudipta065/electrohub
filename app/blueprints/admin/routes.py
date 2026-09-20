from functools import wraps
from decimal import Decimal, InvalidOperation

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ...extensions import db
from ...models import Category, Inventory, Order, Product, Store

bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapped


@bp.get("/")
@admin_required
def dashboard():
    return render_template("admin/dashboard.html", products=Product.query.order_by(Product.name).all(),
                           orders=Order.query.order_by(Order.order_date.desc()).limit(10).all())


@bp.route("/products/new", methods=["GET", "POST"])
@admin_required
def new_product():
    categories = Category.query.order_by(Category.name).all()
    if request.method == "POST":
        try:
            price = Decimal(request.form.get("price", "0"))
            stock = int(request.form.get("stock", "0"))
            if price <= 0 or stock < 0:
                raise ValueError
            if Product.query.filter_by(sku=request.form.get("sku", "").strip()).first():
                raise ValueError("SKU already exists.")
            product = Product(category_id=int(request.form["category_id"]),
                              sku=request.form["sku"].strip(), name=request.form["name"].strip(),
                              brand=request.form.get("brand", "").strip(), price=price,
                              description=request.form.get("description", "").strip(),
                              image_url=request.form.get("image_url", "").strip())
            db.session.add(product)
            db.session.flush()
            store = Store.query.first()
            if not store:
                store = Store(name="Online Warehouse", address="Sydney NSW")
                db.session.add(store)
                db.session.flush()
            db.session.add(Inventory(product=product, store=store, quantity=stock))
            db.session.commit()
            flash("Product created.", "success")
            return redirect(url_for("admin.dashboard"))
        except (ValueError, InvalidOperation, KeyError) as error:
            db.session.rollback()
            flash(str(error) if str(error) else "Check the product information.", "error")
    return render_template("admin/product_form.html", categories=categories)


@bp.post("/orders/<int:order_id>/status")
@admin_required
def update_order_status(order_id):
    order = db.session.get(Order, order_id) or abort(404)
    status = request.form.get("status")
    if status not in {"CONFIRMED", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"}:
        abort(400)
    order.status = status
    db.session.commit()
    flash("Order status updated.", "success")
    return redirect(url_for("admin.dashboard"))

