from pydantic import BaseModel, Field

from app.schemas.knowledge import Concept, FedIDModel


class UserCreationRequest(BaseModel):
    username: str
    password: str = Field(min_length=8)
    # is_curator/is_admin are deliberately absent: self-registration can never
    # grant elevated roles. Roles are only changed via the admin-only role endpoint.


class User(FedIDModel):
    username: str
    is_curator: bool | None = False
    is_admin: bool | None = False
    # Deliberately excludes password/password_hash: this is the schema returned to clients.


class UserRoleUpdate(BaseModel):
    is_curator: bool | None = None
    is_admin: bool | None = None


class UserProfile(BaseModel):
    user: User
    created_concepts: list[Concept]
    commented_concepts: list[Concept]
