from uuid import UUID

from pydantic import BaseModel, field_validator

from app.types import fed_id


class ConceptCreationRequest(BaseModel):
    creator_id: fed_id
    name: str
    description: str | None = None


class Concept(BaseModel):
    id: fed_id
    creator_id: fed_id
    name: str
    description: str | None = None

    @field_validator("id", mode="before")
    def validate_id(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class ConceptLinkCreationRequest(BaseModel):
    creator_id: fed_id
    source_concept_id: fed_id
    target_concept_id: fed_id


class ConceptLink(BaseModel):
    id: fed_id
    creator_id: fed_id
    source_concept_id: fed_id
    target_concept_id: fed_id

    @field_validator("id", mode="before")
    def validate_id(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class CommentCreationRequest(BaseModel):
    commentable_id: fed_id
    creator_id: fed_id
    content: str


class Comment(BaseModel):
    id: fed_id
    commentable_id: fed_id
    creator_id: fed_id
    content: str

    @field_validator("id", mode="before")
    def validate_id(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v