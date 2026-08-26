import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.db import knowledge as db_knowledge
from app.deps import get_current_user, require_curator, require_curator_or_admin
from app.schemas.knowledge import (
    Comment,
    CommentCreationRequest,
    Concept,
    ConceptCreationRequest,
    ConceptDetail,
    ConceptLink,
    ConceptLinkCreationRequest,
)
from app.schemas.users import User

router = APIRouter()


@router.get("/knowledge/concepts")
def get_concepts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Concept]:
    return db_knowledge.get_all_concepts(db)


@router.get("/knowledge/concepts/{concept_id}")
def get_concept(
    concept_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Concept | None:
    return db_knowledge.get_concept_by_id(db, concept_id)


@router.get("/knowledge/concepts/{concept_id}/detail")
def get_concept_detail(
    concept_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ConceptDetail:
    result = db_knowledge.get_concept_detail(db, concept_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Concept not found.")
    return result


@router.post("/knowledge/concepts")
def create_concept(
    concept: ConceptCreationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_curator_or_admin),
) -> Concept:
    return db_knowledge.create_concept(db, current_user.id, concept)


@router.post("/knowledge/concept-links", status_code=status.HTTP_201_CREATED)
def create_concept_link(
    concept_link: ConceptLinkCreationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_curator),
) -> ConceptLink:
    result = db_knowledge.create_concept_link(db, current_user.id, concept_link)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source concept, target concept, or creator was not found.",
        )
    return result


@router.post(
    "/knowledge/comments",
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    comment: CommentCreationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Comment:
    result = db_knowledge.create_comment(db, comment.commentable_id, current_user.id, comment)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commentable record or creator was not found.",
        )
    return result