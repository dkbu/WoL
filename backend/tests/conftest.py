from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from app.main import app
from app.db import get_db


def mock_db():
    db = MagicMock()
    db.execute.return_value = None
    return db


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = mock_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
