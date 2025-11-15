from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Import models after db is created
    from app import models  # noqa: F401
    
    # Register routes (import here to avoid circular import)
    from app.web.routes import register_routes
    register_routes(app)
    
    return app


# Create app instance for gunicorn
Config.validate()
app = create_app()

