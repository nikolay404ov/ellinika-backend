from flask import Flask

from app.config import Config
from app.web.routes import register_routes


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register routes
    register_routes(app)
    
    return app

