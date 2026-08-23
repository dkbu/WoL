from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_health_includes_database_field(client: TestClient) -> None:
    response = client.get("/api/health")
    assert "database" in response.json()


def test_health_database_ok_when_reachable(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.json()["database"] == "ok"
