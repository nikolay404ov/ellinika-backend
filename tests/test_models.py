"""Tests for app/models.py (Word model)."""

from datetime import datetime


class TestWordRepr:
    def test_repr_contains_id_greek_and_translation(self, app):
        from app.models import Word
        word = Word(id=1, greek_word="καλημέρα", translation="доброе утро")
        r = repr(word)
        assert "1" in r
        assert "καλημέρα" in r
        assert "доброе утро" in r

    def test_repr_format(self, app):
        from app.models import Word
        word = Word(id=42, greek_word="νερό", translation="вода")
        assert repr(word) == "<Word(id=42, greek_word='νερό', translation='вода')>"


class TestWordToDict:
    def test_to_dict_contains_all_keys(self, app):
        from app.models import Word
        word = Word(id=1, greek_word="θάλασσα", translation="море")
        d = word.to_dict()
        assert set(d.keys()) == {"id", "greek_word", "translation", "created_at", "updated_at"}

    def test_to_dict_values(self, app):
        from app.models import Word
        word = Word(id=5, greek_word="σπίτι", translation="дом")
        d = word.to_dict()
        assert d["id"] == 5
        assert d["greek_word"] == "σπίτι"
        assert d["translation"] == "дом"

    def test_to_dict_none_timestamps(self, app):
        from app.models import Word
        word = Word(greek_word="γάτα", translation="кошка")
        # created_at / updated_at are None until persisted
        word.created_at = None
        word.updated_at = None
        d = word.to_dict()
        assert d["created_at"] is None
        assert d["updated_at"] is None

    def test_to_dict_timestamps_as_iso_string(self, app):
        from app.models import Word
        now = datetime(2024, 6, 15, 12, 0, 0)
        word = Word(greek_word="ήλιος", translation="солнце")
        word.created_at = now
        word.updated_at = now
        d = word.to_dict()
        assert d["created_at"] == "2024-06-15T12:00:00"
        assert d["updated_at"] == "2024-06-15T12:00:00"


class TestWordPersistence:
    def test_word_can_be_saved_and_retrieved(self, app, db):
        from app.models import Word
        word = Word(greek_word="αγάπη", translation="любовь")
        db.session.add(word)
        db.session.commit()

        fetched = Word.query.filter_by(greek_word="αγάπη").first()
        assert fetched is not None
        assert fetched.translation == "любовь"

    def test_word_id_auto_assigned(self, app, db):
        from app.models import Word
        word = Word(greek_word="ουρανός", translation="небо")
        db.session.add(word)
        db.session.commit()
        assert word.id is not None

    def test_multiple_words_stored_independently(self, app, db):
        from app.models import Word
        w1 = Word(greek_word="μέρα", translation="день")
        w2 = Word(greek_word="νύχτα", translation="ночь")
        db.session.add_all([w1, w2])
        db.session.commit()
        assert Word.query.count() == 2
