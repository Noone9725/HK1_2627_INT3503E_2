import os

from flask import Flask
from flask_smorest import Api
from .extensions import db, migrate
from .config import DefaultConfig
from .api.errors import register_error_handlers
from .api.products import products_bp
from .api.orders import orders_bp
from .api.health import health_bp

def create_app(config=None):
    app = Flask(__name__)
    cfg = config or os.environ.get("APP_CONFIG", DefaultConfig)
    app.config.from_object(cfg)
    
    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)
    api.register_blueprint(products_bp)
    api.register_blueprint(orders_bp)
    api.register_blueprint(health_bp)
    
    register_error_handlers(app)
    
    return app
