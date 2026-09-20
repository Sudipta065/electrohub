from flask import Flask, render_template

from .config import Config
from .extensions import csrf, db, login_manager


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from .blueprints.auth.routes import bp as auth_bp
    from .blueprints.shop.routes import bp as shop_bp
    from .blueprints.cart.routes import bp as cart_bp
    from .blueprints.admin.routes import bp as admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.cli.command("init-db")
    def init_db_command():
        """Create tables and insert demonstration data."""
        from .seed import seed_database
        db.create_all()
        seed_database()
        print("Database initialized.")

    return app

