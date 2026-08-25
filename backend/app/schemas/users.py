from pydantic import BaseModel

from app.schemas.knowledge import Concept, FedIDModel


class UserCreationRequest(BaseModel):
    username: str
    is_curator: bool | None = False  # Default to False if not provided


class User(UserCreationRequest, FedIDModel):
    pass
    # id is inherited from FedIDModel; username and is_curator from UserCreationRequest


class UserProfile(BaseModel):
    user: User
    created_concepts: list[Concept]
    commented_concepts: list[Concept]
