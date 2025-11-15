from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config
from app.web.routes import register_routes

db = SQLAlchemy()


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Register routes
    register_routes(app)
    
    return app


# Create app instance for gunicorn
Config.validate()
app = create_app()

