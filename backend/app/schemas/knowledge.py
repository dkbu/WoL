from uuid import UUID

from pydantic import BaseModel, field_validator

from app.types import fed_id


class FedIDModel(BaseModel):
    """Base model for schemas with a `fed_id` id field, normalizing UUID to str."""

    id: fed_id

    @field_validator("id", mode="before")
    def validate_id(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class ConceptCreationRequest(BaseModel):
    creator_id: fed_id
    name: str
    description: str | None = None


class Concept(FedIDModel):
    creator_id: fed_id
    name: str
    description: str | None = None


class ConceptLinkCreationRequest(BaseModel):
    creator_id: fed_id
    source_concept_id: fed_id
    target_concept_id: fed_id


class ConceptLink(FedIDModel):
    creator_id: fed_id
    source_concept_id: fed_id
    target_concept_id: fed_id


class CommentCreationRequest(BaseModel):
    commentable_id: fed_id
    creator_id: fed_id
    content: str


class Comment(FedIDModel):
    commentable_id: fed_id
    creator_id: fed_id
    content: str


class ConceptCreator(FedIDModel):
    username: str


class LinkedConcept(FedIDModel):
    name: str


class ConceptComment(FedIDModel):
    content: str
    creator: ConceptCreator


class ConceptDetail(FedIDModel):
    name: str
    description: str | None = None
    creator: ConceptCreator
    linked_concepts: list[LinkedConcept]
    comments: list[ConceptComment]