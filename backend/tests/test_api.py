from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.schemas.knowledge import Comment, Concept, ConceptLink

CONCEPT_ID = "123e4567-e89b-12d3-a456-426614174000"
SECOND_CONCEPT_ID = "223e4567-e89b-12d3-a456-426614174000"
CREATOR_ID = "323e4567-e89b-12d3-a456-426614174000"


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
			"id": CONCEPT_ID,
			"creator_id": CREATOR_ID,
			"name": "Museum",
			"description": "A knowledge graph",
		}
	]
	get_all_concepts.assert_called_once()


def test_get_concept_returns_service_result(client: TestClient) -> None:
	concept = Concept(id=CONCEPT_ID, creator_id=CREATOR_ID, name="Museum", description=None)

	with patch(
		"app.api.knowledge.db_knowledge.get_concept_by_id", return_value=concept
	) as get_concept_by_id:
		response = client.get(f"/api/knowledge/concepts/{CONCEPT_ID}")

	assert response.status_code == 200
	assert response.json() == {
		"id": CONCEPT_ID,
		"creator_id": CREATOR_ID,
		"name": "Museum",
		"description": None,
	}
	get_concept_by_id.assert_called_once()


def test_create_concept_returns_created_concept(client: TestClient) -> None:
	payload = {
		"creator_id": CREATOR_ID,
		"name": "Museum",
		"description": "A knowledge graph",
	}
	expected = {"id": CONCEPT_ID, **payload}

	with patch(
		"app.api.knowledge.db_knowledge.create_concept",
		return_value=Concept(**expected),
	) as create_concept:
		response = client.post("/api/knowledge/concepts", json=payload)

	assert response.status_code == 200
	assert response.json() == expected
	create_concept.assert_called_once()


def test_create_concept_link_returns_created_link(client: TestClient) -> None:
	payload = {
		"creator_id": CREATOR_ID,
		"source_concept_id": CONCEPT_ID,
		"target_concept_id": SECOND_CONCEPT_ID,
	}
	expected = {"id": CONCEPT_ID, **payload}

	with patch(
		"app.api.knowledge.db_knowledge.create_concept_link",
		return_value=ConceptLink(**expected),
	) as create_concept_link:
		response = client.post("/api/knowledge/concept-links", json=payload)

	assert response.status_code == 201
	assert response.json() == expected
	create_concept_link.assert_called_once()


def test_create_comment_returns_created_comment(client: TestClient) -> None:
	payload = {
		"commentable_id": CONCEPT_ID,
		"creator_id": CREATOR_ID,
		"content": "Useful context.",
	}
	expected = {"id": SECOND_CONCEPT_ID, **payload}

	with patch(
		"app.api.knowledge.db_knowledge.create_comment",
		return_value=Comment(**expected),
	) as create_comment:
		response = client.post("/api/knowledge/comments", json=payload)

	assert response.status_code == 201
	assert response.json() == expected
	create_comment.assert_called_once()


def test_get_concept_rejects_an_invalid_uuid(client: TestClient) -> None:
	response = client.get("/api/knowledge/concepts/not-a-uuid")

	assert response.status_code == 422
