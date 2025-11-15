import os


class Config:
    """Application configuration."""
    
    # Telegram Bot
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    # PostgreSQL Database
    DB_HOSTNAME = os.environ.get("DB_HOSTNAME")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_DATABASE = os.environ.get("DB_DATABASE")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.TELEGRAM_TOKEN:
            raise RuntimeError("TELEGRAM_TOKEN is not set")
    
    @classmethod
    def get_database_url(cls):
        """Get PostgreSQL database connection URL."""
        if all([cls.DB_HOSTNAME, cls.DB_DATABASE, cls.DB_USER, cls.DB_PASS]):
            return f"postgresql://{cls.DB_USER}:{cls.DB_PASS}@{cls.DB_HOSTNAME}:{cls.DB_PORT}/{cls.DB_DATABASE}"
        return None

