import uuid

from sqlalchemy.orm import Session

from app.models.knowledge import ConceptModel
from app.models.users import UserModel
from app.schemas.knowledge import Concept
from app.schemas.users import User, UserCreationRequest, UserProfile


def _to_concept(concept_model: ConceptModel) -> Concept:
    return Concept(
        id=concept_model.id,
        creator_id=concept_model.creator_id,
        name=concept_model.name,
        description=concept_model.description,
    )


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    """Retrieve a user by their ID from the database."""
    user_model = db.get(UserModel, user_id)
    if not user_model:
        return None
    return User(
        id=user_model.id,
        username=user_model.username,
        is_curator=user_model.is_curator,
    )


def get_user_profile(db: Session, user_id: uuid.UUID) -> UserProfile | None:
    """Build a user's profile from the user's own model relationships."""
    user_model = db.get(UserModel, user_id)
    if not user_model:
        return None

    # commentables includes both concepts and concept links the user created.
    created_concepts = [c for c in user_model.commentables if isinstance(c, ConceptModel)]

    # Comments can be made on concepts or concept links; keep only concept comments.
    commented_concepts = {
        comment.commentable.id: comment.commentable
        for comment in user_model.user_comments
        if isinstance(comment.commentable, ConceptModel)
    }

    return UserProfile(
        user=User(
            id=user_model.id,
            username=user_model.username,
            is_curator=user_model.is_curator,
        ),
        created_concepts=[_to_concept(c) for c in created_concepts],
        commented_concepts=[_to_concept(c) for c in commented_concepts.values()],
    )

def create_user(db: Session, user: UserCreationRequest) -> User:
    """Create a new user in the database."""

    user_model = UserModel(
        username=user.username,
        is_curator=user.is_curator,
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return User(
        id=user_model.id,
        username=user_model.username,
        is_curator=user_model.is_curator,
    )