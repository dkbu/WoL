import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.db import users as db_users
from app.schemas.users import User, UserCreationRequest, UserProfile

router = APIRouter()


@router.get("/users/{user_id}")
def get_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> User:
    result = db_users.get_user_by_id(db, user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return result


@router.get("/users/{user_id}/profile")
def get_user_profile(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> UserProfile:
    result = db_users.get_user_profile(db, user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return result

@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreationRequest,
    db: Session = Depends(get_db),
) -> User:
    """Create a new user in the database."""
    return db_users.create_user(db, user)