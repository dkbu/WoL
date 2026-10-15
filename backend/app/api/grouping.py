from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.db import grouping as db_grouping
from app.deps import get_current_user
from app.schemas.groupings import ChangeConceptRequest
from app.schemas.users import User
from app.types import fed_id

router = APIRouter()


@router.get("/pools/{pool_id}")
def get_pool(
    pool_id: fed_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pool = db_grouping.get_pool_by_id(db, pool_id)
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pool not found",
        )
    return pool


@router.post("/libraries/add_concept")
def add_concept_to_library(
    request: ChangeConceptRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_grouping.add_concept_to_library(
        db, request.library_id, request.concept_id, current_user
    )
    return {"success": True}


@router.post("/libraries/remove_concept")
def remove_concept_from_library(
    request: ChangeConceptRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_grouping.remove_concept_from_library(
        db, request.library_id, request.concept_id, current_user
    )
    return {"success": True}


@router.get("/libraries/{library_id}")
def get_library(
    library_id: fed_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    library = db_grouping.get_library_by_id(db, library_id, current_user)
    if not library:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Library not found",
        )
    return library
