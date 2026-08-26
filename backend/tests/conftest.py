from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from app.main import app
from app.db import get_db
from app.deps import get_current_user
from app.schemas.users import User

TEST_USER_ID = "999e4567-e89b-12d3-a456-426614174999"


def mock_db():
    db = MagicMock()
    db.execute.return_value = None
    return db


def _fake_current_user(is_curator: bool = False, is_admin: bool = False) -> User:
    return User(id=TEST_USER_ID, username="testuser", is_curator=is_curator, is_admin=is_admin)


@pytest.fixture
def client():
    """An authenticated (curator) client: covers the common case for existing tests."""
    app.dependency_overrides[get_db] = mock_db
    app.dependency_overrides[get_current_user] = lambda: _fake_current_user(is_curator=True)
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def anon_client():
    """An unauthenticated client, for testing that auth is actually enforced."""
    app.dependency_overrides[get_db] = mock_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def noncurator_client():
    """An authenticated but non-curator, non-admin client, for testing role restrictions."""
    app.dependency_overrides[get_db] = mock_db
    app.dependency_overrides[get_current_user] = lambda: _fake_current_user()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin_client():
    """An authenticated admin (but non-curator) client, for testing admin-only endpoints."""
    app.dependency_overrides[get_db] = mock_db
    app.dependency_overrides[get_current_user] = lambda: _fake_current_user(is_admin=True)
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
