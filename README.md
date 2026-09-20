# ElectroHub Electronics Store Simple Version

ElectroHub is a three-tier/MVC coursework application for an online electronics store. It uses a Flask web layer, reusable service layer, and SQLAlchemy data layer. The schema is based on the supplied `jbhifi.sql` design and remains portable between local SQLite and hosted PostgreSQL.

The implementation intentionally keeps the code small and direct for an academic demonstration. See `SIMPLE_VIVA_GUIDE.md` for the easiest explanation of the structure and main workflows.

## Implemented features

- Customer registration, login, logout and password hashing
- Responsive product catalogue, category filter and search
- Product details with live total inventory
- Persistent customer carts with stock validation
- Checkout, simulated payment, inventory deduction and order history
- Administrator dashboard, product creation and order-status management
- CSRF protection, role-based access control and server-side validation
- Automated tests for authentication, catalogue, authorization, cart and checkout
- Vercel-compatible Python entry point and configuration

The payment flow is intentionally simulated. It does not request or store real card details.

## Architecture

| Layer | Files | Responsibility |
|---|---|---|
| View | `app/templates`, `app/static` | HTML pages and responsive CSS |
| Controller | `app/blueprints` | HTTP routes, input handling and navigation |
| Business logic | `app/services` | Cart rules, checkout, payments and inventory updates |
| Model/data | `app/models.py` | Entities, relationships and database persistence |

## Local setup

Python 3.11 or later is recommended.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env
flask --app run.py init-db
python run.py
```

Open `http://127.0.0.1:5000`.

Default demonstration administrator:

- Email: `admin@example.com`
- Password: `ChangeMe123!`

Change both values in `.env` before initializing a real database.

## Run the tests

```bash
pytest -v --cov=app --cov-report=term-missing
```

Tests use an isolated in-memory SQLite database and never change the development or production database.

## Deploy to Vercel with PostgreSQL

SQLite must not be used as the production database on Vercel because serverless files are temporary. Create a free PostgreSQL database using Neon, Supabase, Vercel Postgres, or another provider.

1. Push this project to a GitHub repository.
2. Import the repository at Vercel and keep the project root as the root directory.
3. In **Project Settings → Environment Variables**, add:
   - `DATABASE_URL`: the PostgreSQL connection string
   - `SECRET_KEY`: a long random value
   - `ADMIN_EMAIL`: the initial administrator email
   - `ADMIN_PASSWORD`: a strong temporary administrator password
4. Initialize the hosted database once from a trusted computer:

```bash
export DATABASE_URL='postgresql+psycopg://USER:PASSWORD@HOST/DATABASE?sslmode=require'
export ADMIN_EMAIL='your-admin@example.com'
export ADMIN_PASSWORD='use-a-strong-password'
python scripts/init_db.py
```

5. Deploy from Vercel. The `vercel.json` file sends requests to `api/index.py`.

If a provider gives a URL beginning with `postgres://` or `postgresql://`, the application automatically converts it to the current psycopg driver format.

## Suggested Git workflow

```bash
git init
git add .
git commit -m "Create Flask electronics store"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

After the repository is connected to Vercel, later pushes to `main` create new deployments automatically.

## Project structure

```text
jbhifi_store/
├── api/index.py                Vercel entry point
├── app/
│   ├── blueprints/             Controllers grouped by feature
│   ├── services/               Reusable business logic
│   ├── static/css/             Responsive presentation
│   ├── templates/              Jinja HTML views
│   ├── config.py               Environment configuration
│   ├── models.py               Database model layer
│   └── seed.py                 Demonstration records
├── scripts/init_db.py          Hosted database initializer
├── tests/                      Automated test suite
├── run.py                      Local entry point
├── requirements.txt
└── vercel.json
```

## Database design mapping

The application implements all ten supplied tables: `users`, `categories`, `products`, `stores`, `inventory`, `carts`, `cart_items`, `orders`, `order_items`, and `payments`. SQLAlchemy generates syntax appropriate for SQLite or PostgreSQL, avoiding the MySQL-only `AUTO_INCREMENT`, `USE`, and `ENUM` syntax in the original SQL file.
