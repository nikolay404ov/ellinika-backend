"""Tests for app/bot/database.py."""

import pytest


def _add_word(db, greek, translation):
    from app.models import Word
    w = Word(greek_word=greek, translation=translation)
    db.session.add(w)
    db.session.commit()
    return w


class TestGetRandomWord:
    def test_returns_none_when_table_empty(self, app, db):
        from app.bot.database import get_random_word
        assert get_random_word() is None

    def test_returns_word_when_one_exists(self, app, db):
        from app.bot.database import get_random_word
        _add_word(db, "γεια", "привет")
        word = get_random_word()
        assert word is not None
        assert word.greek_word == "γεια"

    def test_returns_one_of_multiple_words(self, app, db):
        from app.bot.database import get_random_word
        _add_word(db, "καλός", "хороший")
        _add_word(db, "κακός", "плохой")
        word = get_random_word()
        assert word.greek_word in ("καλός", "κακός")


class TestGetWordById:
    def test_returns_word_for_valid_id(self, app, db):
        from app.bot.database import get_word_by_id
        w = _add_word(db, "πόλη", "город")
        fetched = get_word_by_id(w.id)
        assert fetched is not None
        assert fetched.greek_word == "πόλη"

    def test_returns_none_for_nonexistent_id(self, app, db):
        from app.bot.database import get_word_by_id
        assert get_word_by_id(99999) is None

    def test_correct_word_returned_among_many(self, app, db):
        from app.bot.database import get_word_by_id
        w1 = _add_word(db, "πατέρας", "отец")
        w2 = _add_word(db, "μητέρα", "мать")
        assert get_word_by_id(w1.id).translation == "отец"
        assert get_word_by_id(w2.id).translation == "мать"


class TestGetAllWords:
    def test_returns_empty_list_when_no_words(self, app, db):
        from app.bot.database import get_all_words
        assert get_all_words() == []

    def test_returns_all_words(self, app, db):
        from app.bot.database import get_all_words
        _add_word(db, "βιβλίο", "книга")
        _add_word(db, "αυτοκίνητο", "машина")
        words = get_all_words()
        assert len(words) == 2

    def test_returned_words_have_correct_data(self, app, db):
        from app.bot.database import get_all_words
        _add_word(db, "φίλος", "друг")
        words = get_all_words()
        assert words[0].greek_word == "φίλος"
        assert words[0].translation == "друг"


class TestAddWord:
    def test_adds_word_and_returns_it(self, app, db):
        from app.bot.database import add_word
        from app.models import Word
        word = add_word("σκύλος", "собака")
        assert word.id is not None
        assert word.greek_word == "σκύλος"
        assert word.translation == "собака"
        assert Word.query.count() == 1

    def test_added_word_is_persisted(self, app, db):
        from app.bot.database import add_word
        from app.models import Word
        add_word("γάτα", "кошка")
        fetched = Word.query.filter_by(greek_word="γάτα").first()
        assert fetched is not None
        assert fetched.translation == "кошка"

    def test_add_multiple_words(self, app, db):
        from app.bot.database import add_word
        from app.models import Word
        add_word("ψωμί", "хлеб")
        add_word("νερό", "вода")
        assert Word.query.count() == 2
