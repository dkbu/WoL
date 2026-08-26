"""FastAPI dependencies for authentication and authorization."""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.db import users as db_users
from app.schemas.users import User
from app.security import decode_access_token

COOKIE_NAME = "access_token"


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    """Resolve the logged-in user from the session cookie, or raise 401."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated."
        )

    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session."
        )

    user = db_users.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exists."
        )
    return user


def require_curator(current_user: User = Depends(get_current_user)) -> User:
    """Same as `get_current_user`, but additionally requires curator status."""
    if not current_user.is_curator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only curators may perform this action.",
        )
    return current_user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Same as `get_current_user`, but additionally requires admin status.

    Admin is a separate permission layer from curator: curators manage the
    knowledge graph content, admins manage users and roles.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins may perform this action.",
        )
    return current_user
