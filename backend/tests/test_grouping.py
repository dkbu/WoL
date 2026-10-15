from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.db import grouping as db_grouping
from app.errors import ConceptNotFoundError, ForbiddenError, LibraryNotFoundError
from app.schemas.users import User
from app.types import fed_id
from tests.conftest import TEST_USER_ID

LIBRARY_ID = fed_id("423e4567-e89b-12d3-a456-426614174000")
POOL_ID = fed_id("523e4567-e89b-12d3-a456-426614174000")
CONCEPT_ID = fed_id("123e4567-e89b-12d3-a456-426614174000")

PAYLOAD = {"concept_id": str(CONCEPT_ID), "library_id": str(LIBRARY_ID)}


@pytest.fixture
def user() -> User:
    return User(
        id=TEST_USER_ID, username="testuser", is_curator=False, is_admin=False
    )


def _library_with(concepts: list[object]) -> SimpleNamespace:
    return SimpleNamespace(concepts=concepts)


# --- DB layer ---


def test_add_concept_to_library_appends_and_commits(user: User) -> None:
    db = MagicMock()
    concept = object()
    library = _library_with([])

    with (
        patch.object(db_grouping, "get_library_by_id", return_value=library),
        patch.object(db_grouping, "get_concept_by_id", return_value=concept),
    ):
        db_grouping.add_concept_to_library(db, LIBRARY_ID, CONCEPT_ID, user)

    assert library.concepts == [concept]
    db.commit.assert_called_once()


def test_add_concept_to_library_missing_library_raises(user: User) -> None:
    db = MagicMock()

    with (
        patch.object(db_grouping, "get_library_by_id", return_value=None),
        patch.object(db_grouping, "get_concept_by_id") as get_concept,
        pytest.raises(LibraryNotFoundError),
    ):
        db_grouping.add_concept_to_library(db, LIBRARY_ID, CONCEPT_ID, user)

    get_concept.assert_not_called()
    db.commit.assert_not_called()


def test_add_concept_to_library_missing_concept_raises(user: User) -> None:
    db = MagicMock()
    library = _library_with([])

    with (
        patch.object(db_grouping, "get_library_by_id", return_value=library),
        patch.object(db_grouping, "get_concept_by_id", return_value=None),
        pytest.raises(ConceptNotFoundError),
    ):
        db_grouping.add_concept_to_library(db, LIBRARY_ID, CONCEPT_ID, user)

    assert library.concepts == []
    db.commit.assert_not_called()


def test_remove_concept_from_library_removes_and_commits(user: User) -> None:
    db = MagicMock()
    concept = object()
    library = _library_with([concept])

    with (
        patch.object(db_grouping, "get_library_by_id", return_value=library),
        patch.object(db_grouping, "get_concept_by_id", return_value=concept),
    ):
        db_grouping.remove_concept_from_library(db, LIBRARY_ID, CONCEPT_ID, user)

    assert library.concepts == []
    db.commit.assert_called_once()


def test_remove_concept_not_in_library_is_noop(user: User) -> None:
    db = MagicMock()
    library = _library_with([])

    with (
        patch.object(db_grouping, "get_library_by_id", return_value=library),
        patch.object(db_grouping, "get_concept_by_id", return_value=object()),
    ):
        db_grouping.remove_concept_from_library(db, LIBRARY_ID, CONCEPT_ID, user)

    db.commit.assert_not_called()


def test_remove_concept_missing_library_raises(user: User) -> None:
    with (
        patch.object(db_grouping, "get_library_by_id", return_value=None),
        pytest.raises(LibraryNotFoundError),
    ):
        db_grouping.remove_concept_from_library(
            MagicMock(), LIBRARY_ID, CONCEPT_ID, user
        )


def test_remove_concept_missing_concept_raises(user: User) -> None:
    with (
        patch.object(db_grouping, "get_library_by_id", return_value=_library_with([])),
        patch.object(db_grouping, "get_concept_by_id", return_value=None),
        pytest.raises(ConceptNotFoundError),
    ):
        db_grouping.remove_concept_from_library(
            MagicMock(), LIBRARY_ID, CONCEPT_ID, user
        )


# --- API layer ---


def test_get_pool_returns_pool(client: TestClient) -> None:
    pool = {"id": str(POOL_ID), "name": "Pool"}

    with patch(
        "app.api.grouping.db_grouping.get_pool_by_id", return_value=pool
    ) as get_pool:
        response = client.get(f"/api/pools/{POOL_ID}")

    assert response.status_code == 200
    assert response.json() == pool
    get_pool.assert_called_once()


def test_get_pool_not_found_returns_404(client: TestClient) -> None:
    with patch("app.api.grouping.db_grouping.get_pool_by_id", return_value=None):
        response = client.get(f"/api/pools/{POOL_ID}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Pool not found"


def test_get_library_returns_library(client: TestClient) -> None:
    library = {"id": str(LIBRARY_ID), "name": "Library"}

    with patch(
        "app.api.grouping.db_grouping.get_library_by_id", return_value=library
    ) as get_library:
        response = client.get(f"/api/libraries/{LIBRARY_ID}")

    assert response.status_code == 200
    assert response.json() == library
    get_library.assert_called_once()


def test_get_library_not_found_returns_404(client: TestClient) -> None:
    with patch("app.api.grouping.db_grouping.get_library_by_id", return_value=None):
        response = client.get(f"/api/libraries/{LIBRARY_ID}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Library not found"


def test_add_concept_to_library_endpoint_succeeds(client: TestClient) -> None:
    with patch("app.api.grouping.db_grouping.add_concept_to_library") as add:
        response = client.post("/api/libraries/add_concept", json=PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {"success": True}
    add.assert_called_once()
    assert add.call_args.args[1:3] == (LIBRARY_ID, CONCEPT_ID)


def test_add_concept_to_library_endpoint_not_found_returns_404(
    client: TestClient,
) -> None:
    with patch(
        "app.api.grouping.db_grouping.add_concept_to_library",
        side_effect=LibraryNotFoundError(LIBRARY_ID),
    ):
        response = client.post("/api/libraries/add_concept", json=PAYLOAD)

    assert response.status_code == 404
    assert str(LIBRARY_ID) in response.json()["detail"]


def test_add_concept_to_library_endpoint_forbidden_returns_403(
    client: TestClient,
) -> None:
    with patch(
        "app.api.grouping.db_grouping.add_concept_to_library",
        side_effect=ForbiddenError(TEST_USER_ID, "library"),
    ):
        response = client.post("/api/libraries/add_concept", json=PAYLOAD)

    assert response.status_code == 403


def test_remove_concept_from_library_endpoint_succeeds(client: TestClient) -> None:
    with patch("app.api.grouping.db_grouping.remove_concept_from_library") as remove:
        response = client.post("/api/libraries/remove_concept", json=PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {"success": True}
    remove.assert_called_once()


def test_remove_concept_from_library_endpoint_not_found_returns_404(
    client: TestClient,
) -> None:
    with patch(
        "app.api.grouping.db_grouping.remove_concept_from_library",
        side_effect=ConceptNotFoundError(CONCEPT_ID),
    ):
        response = client.post("/api/libraries/remove_concept", json=PAYLOAD)

    assert response.status_code == 404
    assert str(CONCEPT_ID) in response.json()["detail"]


def test_add_concept_rejects_invalid_payload(client: TestClient) -> None:
    response = client.post("/api/libraries/add_concept", json={"concept_id": "nope"})

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("get", f"/api/pools/{POOL_ID}"),
        ("get", f"/api/libraries/{LIBRARY_ID}"),
        ("post", "/api/libraries/add_concept"),
        ("post", "/api/libraries/remove_concept"),
    ],
)
def test_grouping_endpoints_require_authentication(
    anon_client: TestClient, method: str, path: str
) -> None:
    response = getattr(anon_client, method)(path)

    assert response.status_code == 401
