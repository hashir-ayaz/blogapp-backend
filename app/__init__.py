# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import and register blueprints after app is created
    from app.routes.user_routes import user_bp
    from app.routes.post_routes import post_bp

    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(post_bp, url_prefix="/api/post")

    return app
