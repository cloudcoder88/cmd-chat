# tests/test_health.py
import pytest


class TestHealth:
    """Тесты health endpoint"""

    def test_health_ok(self, test_client):
        """GET /health возвращает статус"""
        _, response = test_client.get("/health")

        assert response.status == 200
        data = response.json
        assert data["status"] == "ok"
        assert "messages" in data
        assert "users" in data
        assert "timestamp" in data