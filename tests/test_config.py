"""Tests for app/config.py."""

import os
import pytest


class TestConfigValidate:
    def test_validate_raises_when_token_missing(self):
        from app.config import Config
        original = Config.TELEGRAM_TOKEN
        Config.TELEGRAM_TOKEN = None
        try:
            with pytest.raises(RuntimeError, match="TELEGRAM_TOKEN is not set"):
                Config.validate()
        finally:
            Config.TELEGRAM_TOKEN = original

    def test_validate_passes_when_token_set(self):
        from app.config import Config
        original = Config.TELEGRAM_TOKEN
        Config.TELEGRAM_TOKEN = "some-token"
        try:
            Config.validate()  # should not raise
        finally:
            Config.TELEGRAM_TOKEN = original


class TestConfigGetDatabaseUrl:
    def _set_db_env(self, hostname="localhost", port="5432", database="mydb",
                    user="user", password="pass"):
        from app.config import Config
        Config.DB_HOSTNAME = hostname
        Config.DB_PORT = port
        Config.DB_DATABASE = database
        Config.DB_USER = user
        Config.DB_PASS = password

    def _clear_db_env(self):
        from app.config import Config
        Config.DB_HOSTNAME = None
        Config.DB_DATABASE = None
        Config.DB_USER = None
        Config.DB_PASS = None

    def test_returns_url_when_all_vars_set(self):
        from app.config import Config
        self._set_db_env()
        try:
            url = Config.get_database_url()
            assert url == "postgresql://user:pass@localhost:5432/mydb"
        finally:
            self._clear_db_env()

    def test_returns_none_when_hostname_missing(self):
        from app.config import Config
        self._set_db_env(hostname="")
        try:
            assert Config.get_database_url() is None
        finally:
            self._clear_db_env()

    def test_returns_none_when_database_missing(self):
        from app.config import Config
        self._set_db_env()
        Config.DB_DATABASE = None
        try:
            assert Config.get_database_url() is None
        finally:
            self._clear_db_env()

    def test_returns_none_when_user_missing(self):
        from app.config import Config
        self._set_db_env()
        Config.DB_USER = None
        try:
            assert Config.get_database_url() is None
        finally:
            self._clear_db_env()

    def test_returns_none_when_password_missing(self):
        from app.config import Config
        self._set_db_env()
        Config.DB_PASS = None
        try:
            assert Config.get_database_url() is None
        finally:
            self._clear_db_env()

    def test_custom_port_is_included_in_url(self):
        from app.config import Config
        self._set_db_env(port="5433")
        try:
            url = Config.get_database_url()
            assert ":5433/" in url
        finally:
            self._clear_db_env()

    def test_default_port_is_5432(self):
        """DB_PORT should default to '5432' when the env var is absent."""
        from app.config import Config
        original_port = Config.DB_PORT
        Config.DB_PORT = os.environ.get("DB_PORT", "5432")
        self._set_db_env()
        try:
            url = Config.get_database_url()
            assert ":5432/" in url
        finally:
            Config.DB_PORT = original_port
            self._clear_db_env()
