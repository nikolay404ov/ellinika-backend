"""Shared pytest fixtures."""

import os
import pytest

# Set required env vars before any app import
os.environ.setdefault("TELEGRAM_TOKEN", "test-token-123")


@pytest.fixture
def app():
    """Create a Flask test app with an in-memory SQLite database."""
    os.environ["TELEGRAM_TOKEN"] = "test-token-123"
    # Override DB to use SQLite in-memory so no real Postgres is needed
    os.environ["DB_HOSTNAME"] = ""

    from app import create_app, db as _db
    from app.config import Config

    # Patch get_database_url to return SQLite URI for tests
    original_get_db_url = Config.get_database_url.__func__

    @classmethod
    def sqlite_db_url(cls):
        return "sqlite:///:memory:"

    Config.get_database_url = sqlite_db_url

    flask_app = create_app()
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.drop_all()

    # Restore original method
    Config.get_database_url = classmethod(original_get_db_url)


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Database session bound to the test app context."""
    from app import db as _db
    return _db
