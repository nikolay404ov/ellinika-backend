"""Database utilities for bot."""

from app import db
from app.models import Word


def get_random_word():
    """Get a random word from database."""
    return Word.query.order_by(db.func.random()).first()


def get_word_by_id(word_id):
    """Get word by ID."""
    return Word.query.get(word_id)


def get_all_words():
    """Get all words."""
    return Word.query.all()


def add_word(greek_word, translation):
    """Add a new word to database."""
    word = Word(greek_word=greek_word, translation=translation)
    db.session.add(word)
    db.session.commit()
    return word

