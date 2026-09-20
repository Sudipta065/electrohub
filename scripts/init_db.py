"""Initialize and seed the database configured by DATABASE_URL."""
import sys
from pathlib import Path

# Make the project package importable when this file is run directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.extensions import db
from app.seed import seed_database

app = create_app()
with app.app_context():
    db.create_all()
    seed_database()
    print("Database tables and demonstration records are ready.")
