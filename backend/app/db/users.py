import uuid

from sqlalchemy.orm import Session

from app.models.knowledge import ConceptModel
from app.models.users import FollowModel, UserModel
from app.schemas.knowledge import Concept
from app.schemas.users import User, UserCreationRequest, UserProfile
from app.security import hash_password, verify_password


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
    return _to_user(user_model)


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
        user=_to_user(user_model),
        created_concepts=[_to_concept(c) for c in created_concepts],
        commented_concepts=[_to_concept(c) for c in commented_concepts.values()],
    )

def _to_user(user_model: UserModel) -> User:
    return User(
        id=user_model.id,
        username=user_model.username,
        is_curator=user_model.is_curator,
        is_admin=user_model.is_admin,
    )


def get_all_users(db: Session) -> list[User]:
    """Retrieve every user. Intended for admin use only."""
    return [_to_user(u) for u in db.query(UserModel).all()]


def search_users_by_username(db: Session, username: str) -> list[User]:
    """Case-insensitive partial match on username."""
    users = db.query(UserModel).filter(UserModel.username.ilike(f"%{username}%")).all()
    return [_to_user(u) for u in users]


def create_user(db: Session, user: UserCreationRequest) -> User:
    """Create a new user in the database. Always starts with no elevated roles."""

    user_model = UserModel(
        username=user.username,
        password_hash=hash_password(user.password),
        is_curator=False,
        is_admin=False,
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return _to_user(user_model)


def set_user_roles(
    db: Session,
    user_id: uuid.UUID,
    is_curator: bool | None = None,
    is_admin: bool | None = None,
) -> User | None:
    """Grant or revoke curator/admin status. Admin-only; None leaves a field unchanged."""
    user_model = db.get(UserModel, user_id)
    if not user_model:
        return None

    if is_curator is not None:
        user_model.is_curator = is_curator
    if is_admin is not None:
        user_model.is_admin = is_admin

    db.commit()
    db.refresh(user_model)
    return _to_user(user_model)


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """Verify credentials and return the user, or None if invalid."""
    user_model = db.query(UserModel).filter(UserModel.username == username).first()
    if not user_model or not verify_password(password, user_model.password_hash):
        return None
    return _to_user(user_model)


def follow_user(db: Session, follower_id: uuid.UUID, followed_id: uuid.UUID) -> User | None:
    """Make follower_id follow followed_id. Returns the followed user, or None if either doesn't exist."""
    follower = db.get(UserModel, follower_id)
    followed = db.get(UserModel, followed_id)
    if not follower or not followed:
        return None

    existing = (
        db.query(FollowModel)
        .filter(FollowModel.follower_id == follower_id, FollowModel.followed_id == followed_id)
        .first()
    )
    if not existing:
        db.add(FollowModel(follower_id=follower_id, followed_id=followed_id))
        db.commit()

    return _to_user(followed)


def unfollow_user(db: Session, follower_id: uuid.UUID, followed_id: uuid.UUID) -> bool:
    """Stop follower_id following followed_id. Returns whether a follow existed."""
    existing = (
        db.query(FollowModel)
        .filter(FollowModel.follower_id == follower_id, FollowModel.followed_id == followed_id)
        .first()
    )
    if not existing:
        return False
    db.delete(existing)
    db.commit()
    return True


def get_following(db: Session, user_id: uuid.UUID) -> list[User] | None:
    """List the users that user_id follows, or None if the user doesn't exist."""
    user_model = db.get(UserModel, user_id)
    if not user_model:
        return None
    return [_to_user(follow.followed) for follow in user_model.following]