from uuid import UUID

from pydantic import BaseModel, field_validator

from app.schemas.knowledge import Concept
from app.types import fed_id


class UserCreationRequest(BaseModel):
    username: str
    is_curator: bool | None = False  # Default to False if not provided


class User(UserCreationRequest):
    id: fed_id
    # username and is_curator are inherited from UserCreationRequest

    @field_validator("id", mode="before")
    def validate_id(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class UserProfile(BaseModel):
    user: User
    created_concepts: list[Concept]
    commented_concepts: list[Concept]
