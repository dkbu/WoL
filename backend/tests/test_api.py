from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.schemas.knowledge import Concept

CONCEPT_ID = "123e4567-e89b-12d3-a456-426614174000"


def test_list_concepts_returns_service_results(client: TestClient) -> None:
	concepts = [Concept(id=CONCEPT_ID, name="Museum", description="A knowledge graph")]

	with patch(
		"app.api.knowledge.db_knowledge.get_all_concepts", return_value=concepts
	) as get_all_concepts:
		response = client.get("/api/knowledge/concepts")

	assert response.status_code == 200
	assert response.json() == [
		{"id": CONCEPT_ID, "name": "Museum", "description": "A knowledge graph"}
	]
	get_all_concepts.assert_called_once()


def test_get_concept_returns_service_result(client: TestClient) -> None:
	concept = Concept(id=CONCEPT_ID, name="Museum", description=None)

	with patch(
		"app.api.knowledge.db_knowledge.get_concept_by_id", return_value=concept
	) as get_concept_by_id:
		response = client.get(f"/api/knowledge/concepts/{CONCEPT_ID}")

	assert response.status_code == 200
	assert response.json() == {"id": CONCEPT_ID, "name": "Museum", "description": None}
	get_concept_by_id.assert_called_once()


def test_create_concept_returns_created_concept(client: TestClient) -> None:
	payload = {"id": CONCEPT_ID, "name": "Museum", "description": "A knowledge graph"}

	with patch(
		"app.api.knowledge.db_knowledge.create_concept",
		return_value=Concept(**payload),
	) as create_concept:
		response = client.post("/api/knowledge/concepts", json=payload)

	assert response.status_code == 200
	assert response.json() == payload
	create_concept.assert_called_once()


def test_get_concept_rejects_an_invalid_uuid(client: TestClient) -> None:
	response = client.get("/api/knowledge/concepts/not-a-uuid")

	assert response.status_code == 422
