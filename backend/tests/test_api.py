from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.schemas.knowledge import Comment, Concept, ConceptLink
from app.schemas.users import User
from app.types import fed_id
from tests.conftest import TEST_USER_ID

CONCEPT_ID = fed_id("123e4567-e89b-12d3-a456-426614174000")
SECOND_CONCEPT_ID = fed_id("223e4567-e89b-12d3-a456-426614174000")
CREATOR_ID = fed_id("323e4567-e89b-12d3-a456-426614174000")


def test_list_concepts_returns_service_results(client: TestClient) -> None:
    concepts = [
        Concept(
            id=CONCEPT_ID,
            creator_id=CREATOR_ID,
            name="Museum",
            description="A knowledge graph",
        )
    ]

    with patch(
        "app.api.knowledge.db_knowledge.get_all_concepts", return_value=concepts
    ) as get_all_concepts:
        response = client.get("/api/knowledge/concepts")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(CONCEPT_ID),
            "creator_id": str(CREATOR_ID),
            "name": "Museum",
            "description": "A knowledge graph",
        }
    ]
    get_all_concepts.assert_called_once()


def test_get_concept_returns_service_result(client: TestClient) -> None:
    concept = Concept(
        id=CONCEPT_ID, creator_id=CREATOR_ID, name="Museum", description=None
    )

    with patch(
        "app.api.knowledge.db_knowledge.get_concept_by_id", return_value=concept
    ) as get_concept_by_id:
        response = client.get(f"/api/knowledge/concepts/{CONCEPT_ID}")

    assert response.status_code == 200
    assert response.json() == {
        "id": str(CONCEPT_ID),
        "creator_id": str(CREATOR_ID),
        "name": "Museum",
        "description": None,
    }
    get_concept_by_id.assert_called_once()


def test_create_concept_returns_created_concept(client: TestClient) -> None:
    payload = {
        "name": "Museum",
        "description": "A knowledge graph",
    }
    expected = {
        "id": str(CONCEPT_ID),
        "creator_id": str(TEST_USER_ID),
        **payload,
    }

    with patch(
        "app.api.knowledge.db_knowledge.create_concept",
        return_value=Concept(id=CONCEPT_ID, creator_id=TEST_USER_ID, **payload),
    ) as create_concept:
        response = client.post("/api/knowledge/concepts", json=payload)

    assert response.status_code == 200
    assert response.json() == expected
    create_concept.assert_called_once()


def test_create_concept_requires_curator(noncurator_client: TestClient) -> None:
    payload = {"name": "Museum", "description": "A knowledge graph"}

    response = noncurator_client.post("/api/knowledge/concepts", json=payload)

    assert response.status_code == 403


def test_create_concept_allows_admin(admin_client: TestClient) -> None:
    payload = {"name": "Museum", "description": "A knowledge graph"}
    expected = {"id": str(CONCEPT_ID), "creator_id": TEST_USER_ID, **payload}

    with patch(
        "app.api.knowledge.db_knowledge.create_concept",
        return_value=Concept(**expected),
    ):
        response = admin_client.post("/api/knowledge/concepts", json=payload)

    assert response.status_code == 200


def test_create_concept_requires_login(anon_client: TestClient) -> None:
    payload = {"name": "Museum", "description": "A knowledge graph"}

    response = anon_client.post("/api/knowledge/concepts", json=payload)

    assert response.status_code == 401


def test_create_concept_link_returns_created_link(client: TestClient) -> None:
    payload = {
        "source_concept_id": str(CONCEPT_ID),
        "target_concept_id": str(SECOND_CONCEPT_ID),
    }
    expected = {"id": str(CONCEPT_ID), "creator_id": str(TEST_USER_ID), **payload}

    with patch(
        "app.api.knowledge.db_knowledge.create_concept_link",
        return_value=ConceptLink(
            id=CONCEPT_ID,
            creator_id=TEST_USER_ID,
            source_concept_id=CONCEPT_ID,
            target_concept_id=SECOND_CONCEPT_ID,
        ),
    ) as create_concept_link:
        response = client.post("/api/knowledge/concept-links", json=payload)

    assert response.status_code == 201
    assert response.json() == expected
    create_concept_link.assert_called_once()


def test_create_comment_returns_created_comment(client: TestClient) -> None:
    payload = {
        "commentable_id": str(CONCEPT_ID),
        "content": "Useful context.",
    }
    expected = {
        "id": str(SECOND_CONCEPT_ID),
        "creator_id": str(TEST_USER_ID),
        **payload,
    }

    with patch(
        "app.api.knowledge.db_knowledge.create_comment",
        return_value=Comment(
            id=SECOND_CONCEPT_ID,
            creator_id=TEST_USER_ID,
            commentable_id=CONCEPT_ID,
            content="Useful context.",
        ),
    ) as create_comment:
        response = client.post("/api/knowledge/comments", json=payload)

    assert response.status_code == 201
    assert response.json() == expected
    create_comment.assert_called_once()


def test_create_comment_only_requires_login_not_curator(
    noncurator_client: TestClient,
) -> None:
    payload = {"commentable_id": str(CONCEPT_ID), "content": "Useful context."}
    expected = {
        "id": str(SECOND_CONCEPT_ID),
        "creator_id": str(TEST_USER_ID),
        **payload,
    }

    with patch(
        "app.api.knowledge.db_knowledge.create_comment",
        return_value=Comment(
            id=SECOND_CONCEPT_ID,
            creator_id=TEST_USER_ID,
            commentable_id=CONCEPT_ID,
            content="Useful context.",
        ),
    ):
        response = noncurator_client.post("/api/knowledge/comments", json=payload)

    assert response.status_code == 201


def test_get_concept_rejects_an_invalid_uuid(client: TestClient) -> None:
    response = client.get("/api/knowledge/concepts/not-a-uuid")

    assert response.status_code == 422


def test_get_user_rejects_an_invalid_uuid(client: TestClient) -> None:
    response = client.get("/api/users/not-a-uuid")

    assert response.status_code == 422


def test_get_user_profile_rejects_an_invalid_uuid(client: TestClient) -> None:
    response = client.get("/api/users/not-a-uuid/profile")

    assert response.status_code == 422


def test_create_user_successfully(client: TestClient) -> None:
    payload = {
        "username": "testuser",
        "password": "hunter2password",
    }
    expected = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "username": "testuser",
        "is_curator": False,
        "is_admin": False,
    }

    with patch(
        "app.api.users.db_users.create_user",
        return_value=User(**expected),
    ) as create_user:
        response = client.post("/api/users", json=payload)

    assert response.status_code == 201
    assert response.json() == expected
    create_user.assert_called_once()


def test_create_user_does_not_require_login(anon_client: TestClient) -> None:
    payload = {
        "username": "testuser",
        "password": "hunter2password",
    }
    expected = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "username": "testuser",
        "is_curator": False,
        "is_admin": False,
    }

    with patch("app.api.users.db_users.create_user", return_value=User(**expected)):
        response = anon_client.post("/api/users", json=payload)

    assert response.status_code == 201


def test_get_user_requires_login(anon_client: TestClient) -> None:
    response = anon_client.get(f"/api/users/{CREATOR_ID}")

    assert response.status_code == 401


def test_get_user_successfully(client: TestClient) -> None:
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    expected = {
        "id": user_id,
        "username": "testuser",
        "is_curator": True,
        "is_admin": False,
    }

    with patch(
        "app.api.users.db_users.get_user_by_id",
        return_value=User(**expected),
    ):
        response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 200
    assert response.json() == expected


def test_get_user_profile_successfully(client: TestClient) -> None:
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    expected = {
        "user": {
            "id": user_id,
            "username": "testuser",
            "is_curator": True,
            "is_admin": False,
        },
        "created_concepts": [],
        "commented_concepts": [],
    }

    with patch(
        "app.api.users.db_users.get_user_profile",
        return_value=expected,
    ):
        response = client.get(f"/api/users/{user_id}/profile")

    assert response.status_code == 200
    assert response.json() == expected
