import os


class Config:
    """Application configuration."""
    
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.TELEGRAM_TOKEN:
            raise RuntimeError("TELEGRAM_TOKEN is not set")

