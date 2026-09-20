# ElectroHub Simple Code and Viva Guide

## One sentence explanation

ElectroHub is a Flask web application where customers browse electronics, add products to a cart and create orders, while administrators add products and update orders using a PostgreSQL database.

## Easy architecture

The application has four clear parts:

1. **Views:** HTML templates and CSS display the pages.
2. **Controllers:** Blueprint route files receive browser requests.
3. **Services:** Two small files contain cart and checkout rules.
4. **Models:** `models.py` maps Python classes to PostgreSQL tables.

```text
Browser -> Route -> Service -> Model -> PostgreSQL
```

## Files to remember

| File | Simple purpose |
|---|---|
| `run.py` | Starts the application locally |
| `api/index.py` | Starts the application on Vercel |
| `app/__init__.py` | Creates Flask and registers features |
| `app/config.py` | Loads `.env` and the database connection |
| `app/models.py` | Defines all ten database tables |
| `blueprints/auth/routes.py` | Registration, login and logout |
| `blueprints/shop/routes.py` | Home, catalogue, search and product details |
| `blueprints/cart/routes.py` | Cart, checkout and order history pages |
| `blueprints/admin/routes.py` | Administrator dashboard and management |
| `services/cart_service.py` | Cart calculations and stock checking |
| `services/order_service.py` | Creates orders, payment and stock deduction |
| `seed.py` | Inserts sample products and the administrator |

## Database structure

The original database structure is preserved:

- `users`: customer and administrator accounts
- `categories`: product categories
- `products`: electronics sold by the store
- `stores`: store or warehouse locations
- `inventory`: quantity of each product in each store
- `carts`: customer carts
- `cart_items`: products inside carts
- `orders`: completed customer orders
- `order_items`: products copied into orders
- `payments`: simulated payment information

## Main application flow

### Customer registration

The registration route validates the form, checks for an existing email, hashes the password, saves the user and logs the user in.

### Add to cart

The cart route calls `add_product()`. The service checks the product and stock, then creates or updates a cart item.

### Checkout

The checkout service validates the address and payment method, checks stock, creates an order, copies cart items to order items, reduces inventory, creates a simulated payment and empties the cart.

### Administrator

The `admin_required` decorator permits only users whose role is `ADMIN`. Administrators can add a product and inventory or update an order status.

## Ten short viva answers

1. **Why Flask?** Flask supplies web routes, form handling, templates and sessions while Python supplies the programming language.
2. **Why SQLAlchemy?** It maps Python classes to SQL tables and reduces repeated SQL code.
3. **Why PostgreSQL?** It supports reliable relations, foreign keys, constraints and transactions.
4. **Why Neon?** Neon hosts PostgreSQL online so local and Vercel applications share persistent data.
5. **What is MVC?** Models manage data, views display HTML, and controllers handle requests.
6. **Why a service layer?** It keeps cart and checkout rules separate from webpage routes.
7. **How are passwords protected?** Only generated password hashes are stored.
8. **How is admin access protected?** `admin_required` checks that the logged-in user has the `ADMIN` role.
9. **Why check stock twice?** Stock may change between adding an item and completing checkout.
10. **Is payment real?** No. It is simulated so no card information is collected or stored.

## Simple demonstration order

1. Show the product catalogue and search.
2. Register or log in as a customer.
3. Add a product to the cart.
4. Complete checkout and show order history.
5. Log in as administrator.
6. Open `/admin/`, add a product and update an order status.
7. Show the matching tables in Neon.

