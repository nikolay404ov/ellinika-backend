"""Tests for app/web/routes.py."""

from unittest.mock import MagicMock, patch


class TestHealthCheck:
    def test_index_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_body_confirms_bot_running(self, client):
        response = client.get("/")
        assert b"running" in response.data.lower()


class TestWebhookEndpoint:
    """The webhook route is registered at /<TELEGRAM_TOKEN>.
    In tests the token is 'test-token-123'."""

    WEBHOOK_PATH = "/test-token-123"

    def _post_update(self, client, payload):
        return client.post(
            self.WEBHOOK_PATH,
            json=payload,
            content_type="application/json",
        )

    def _minimal_update_payload(self):
        return {
            "update_id": 1,
            "message": {
                "message_id": 1,
                "date": 1700000000,
                "chat": {"id": 1, "type": "private"},
                "from": {"id": 42, "is_bot": False, "first_name": "Test"},
                "text": "/start",
            },
        }

    def test_webhook_returns_ok(self, client):
        payload = self._minimal_update_payload()
        with patch("app.web.routes.ensure_loop_running"), \
             patch("app.web.routes.Update.de_json", return_value=MagicMock()), \
             patch("app.web.routes.get_loop", return_value=MagicMock()), \
             patch("app.web.routes.get_bot_ready_event", return_value=None), \
             patch("app.web.routes.asyncio.run_coroutine_threadsafe") as mock_rct:
            future_mock = MagicMock()
            future_mock.add_done_callback = MagicMock()
            mock_rct.return_value = future_mock

            response = self._post_update(client, payload)

        assert response.status_code == 200
        assert response.data == b"ok"

    def test_webhook_calls_ensure_loop_running(self, client):
        payload = self._minimal_update_payload()
        with patch("app.web.routes.ensure_loop_running") as mock_ensure, \
             patch("app.web.routes.Update.de_json", return_value=MagicMock()), \
             patch("app.web.routes.get_loop", return_value=MagicMock()), \
             patch("app.web.routes.get_bot_ready_event", return_value=None), \
             patch("app.web.routes.asyncio.run_coroutine_threadsafe") as mock_rct:
            future_mock = MagicMock()
            future_mock.add_done_callback = MagicMock()
            mock_rct.return_value = future_mock

            self._post_update(client, payload)

        mock_ensure.assert_called_once()

    def test_webhook_deserialises_update(self, client):
        payload = self._minimal_update_payload()
        with patch("app.web.routes.ensure_loop_running"), \
             patch("app.web.routes.Update.de_json") as mock_de_json, \
             patch("app.web.routes.get_loop", return_value=MagicMock()), \
             patch("app.web.routes.get_bot_ready_event", return_value=None), \
             patch("app.web.routes.asyncio.run_coroutine_threadsafe") as mock_rct:
            mock_de_json.return_value = MagicMock()
            future_mock = MagicMock()
            future_mock.add_done_callback = MagicMock()
            mock_rct.return_value = future_mock

            self._post_update(client, payload)

        mock_de_json.assert_called_once()
        received_data = mock_de_json.call_args[0][0]
        assert received_data["update_id"] == 1

    def test_unknown_route_returns_404(self, client):
        response = client.get("/nonexistent")
        assert response.status_code == 404
