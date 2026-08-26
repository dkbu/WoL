from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.schemas.users import User

USER_ID = "123e4567-e89b-12d3-a456-426614174000"


def test_list_all_users_requires_admin_not_just_curator(client: TestClient) -> None:
    """`client` is a curator but not an admin: admin endpoints must still reject it."""
    response = client.get("/api/admin/users")

    assert response.status_code == 403


def test_list_all_users_rejects_anonymous(anon_client: TestClient) -> None:
    response = anon_client.get("/api/admin/users")

    assert response.status_code == 401


def test_list_all_users_allows_admin(admin_client: TestClient) -> None:
    with patch("app.api.admin.db_users.get_all_users", return_value=[]):
        response = admin_client.get("/api/admin/users")

    assert response.status_code == 200


def test_update_user_roles_allows_admin(admin_client: TestClient) -> None:
    updated = User(id=USER_ID, username="testuser", is_curator=True, is_admin=False)

    with patch("app.api.admin.db_users.set_user_roles", return_value=updated) as set_roles:
        response = admin_client.patch(
            f"/api/admin/users/{USER_ID}/roles", json={"is_curator": True}
        )

    assert response.status_code == 200
    assert response.json()["is_curator"] is True
    set_roles.assert_called_once()


def test_update_user_roles_rejects_non_admin(client: TestClient) -> None:
    response = client.patch(f"/api/admin/users/{USER_ID}/roles", json={"is_curator": True})

    assert response.status_code == 403


def test_update_user_roles_rejects_unknown_user(admin_client: TestClient) -> None:
    with patch("app.api.admin.db_users.set_user_roles", return_value=None):
        response = admin_client.patch(
            f"/api/admin/users/{USER_ID}/roles", json={"is_admin": True}
        )

    assert response.status_code == 404
