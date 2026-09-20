from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ...models import Order
from ...services.cart_service import CartError, add_product, get_or_create_cart, update_item
from ...services.order_service import checkout

bp = Blueprint("cart", __name__, url_prefix="/account")


@bp.get("/cart")
@login_required
def view_cart():
    return render_template("cart/cart.html", cart=get_or_create_cart(current_user.user_id))


@bp.post("/cart/add/<int:product_id>")
@login_required
def add(product_id):
    try:
        add_product(current_user.user_id, product_id, request.form.get("quantity", 1, type=int))
        flash("Product added to your cart.", "success")
    except CartError as error:
        flash(str(error), "error")
    return redirect(request.referrer or url_for("shop.catalog"))


@bp.post("/cart/item/<int:item_id>")
@login_required
def update(item_id):
    try:
        update_item(current_user.user_id, item_id, request.form.get("quantity", 1, type=int))
        flash("Cart updated.", "success")
    except CartError as error:
        flash(str(error), "error")
    return redirect(url_for("cart.view_cart"))


@bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout_page():
    cart = get_or_create_cart(current_user.user_id)
    if request.method == "POST":
        try:
            order = checkout(current_user.user_id, request.form.get("address", ""),
                             request.form.get("payment_method", ""))
            flash(f"Order #{order.order_id} was placed successfully.", "success")
            return redirect(url_for("cart.orders"))
        except CartError as error:
            flash(str(error), "error")
    return render_template("cart/checkout.html", cart=cart)


@bp.get("/orders")
@login_required
def orders():
    orders_list = Order.query.filter_by(user_id=current_user.user_id).order_by(Order.order_date.desc()).all()
    return render_template("cart/orders.html", orders=orders_list)

