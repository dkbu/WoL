from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.schemas.users import User

USER_ID = "123e4567-e89b-12d3-a456-426614174000"


def test_login_success_sets_cookie(anon_client: TestClient) -> None:
    user = User(id=USER_ID, username="testuser", is_curator=False)

    with patch("app.api.auth.db_users.authenticate_user", return_value=user):
        response = anon_client.post(
            "/api/auth/login", json={"username": "testuser", "password": "hunter2password"}
        )

    assert response.status_code == 200
    assert response.json() == {
        "id": USER_ID,
        "username": "testuser",
        "is_curator": False,
        "is_admin": False,
    }
    assert "access_token" in response.cookies


def test_login_rejects_bad_credentials(anon_client: TestClient) -> None:
    with patch("app.api.auth.db_users.authenticate_user", return_value=None):
        response = anon_client.post(
            "/api/auth/login", json={"username": "testuser", "password": "wrong"}
        )

    assert response.status_code == 401


def test_me_requires_login(anon_client: TestClient) -> None:
    response = anon_client.get("/api/auth/me")

    assert response.status_code == 401


def test_me_returns_current_user(client: TestClient) -> None:
    response = client.get("/api/auth/me")

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_logout_clears_cookie(client: TestClient) -> None:
    response = client.post("/api/auth/logout")

    assert response.status_code == 204
