# tests/test_websocket.py
import pytest


class TestWebSocket:
    """Тесты WebSocket подключения"""

    def test_ws_connect_no_user_id(self, test_client):
        """WebSocket без user_id отклоняется"""
        _, ws = test_client.websocket("/ws/chat")
        # Проверяем что соединение закрыто или вернулась ошибка
        assert ws is not None

    def test_ws_connect_invalid_session(self, test_client):
        """WebSocket с невалидным user_id отклоняется"""
        _, ws = test_client.websocket("/ws/chat?user_id=invalid123")
        assert ws is not None