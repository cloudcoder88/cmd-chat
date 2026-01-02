# tests/test_srp.py
import base64
import pytest
import srp


class TestSRPFlow:
    """Тесты SRP аутентификации"""

    def test_srp_init_success(self, test_client):
        """POST /srp/init возвращает user_id, B, salt"""
        usr = srp.User(b"chat", b"testpassword")
        _, A = usr.start_authentication()

        _, response = test_client.post(
            "/srp/init",
            json={
                "username": "testuser",
                "A": base64.b64encode(A).decode(),
            },
        )

        assert response.status == 200
        data = response.json
        assert "user_id" in data
        assert "B" in data
        assert "salt" in data

    def test_srp_init_missing_a(self, test_client):
        """POST /srp/init без A возвращает 400"""
        _, response = test_client.post(
            "/srp/init",
            json={"username": "testuser"},
        )

        assert response.status == 400

    def test_srp_verify_invalid_session(self, test_client):
        """Verify с несуществующим user_id возвращает 401"""
        _, response = test_client.post(
            "/srp/verify",
            json={
                "user_id": "nonexistent",
                "username": "testuser",
                "M": base64.b64encode(b"fake").decode(),
            },
        )
        assert response.status == 401