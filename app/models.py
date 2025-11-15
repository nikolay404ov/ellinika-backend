"""Database models."""

from datetime import datetime

from app import db


class Word(db.Model):
    """Model for Greek words with translations."""
    
    __tablename__ = "words"
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    greek_word = db.Column(db.String(255), nullable=False, index=True)
    translation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Word(id={self.id}, greek_word='{self.greek_word}', translation='{self.translation}')>"
    
    def to_dict(self):
        """Convert word to dictionary."""
        return {
            'id': self.id,
            'greek_word': self.greek_word,
            'translation': self.translation,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

