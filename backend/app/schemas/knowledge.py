from uuid import UUID

from pydantic import BaseModel, field_validator


class ConceptCreationRequest(BaseModel):
    name: str
    description: str | None = None


class Concept(BaseModel):
    id: str | UUID 
    name: str
    description: str | None = None

    @field_validator("id", mode="before")
    def validate_id(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v