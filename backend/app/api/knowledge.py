import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.db import knowledge as db_knowledge
from app.schemas.knowledge import (
    Comment,
    CommentCreationRequest,
    Concept,
    ConceptCreationRequest,
    ConceptDetail,
    ConceptLink,
    ConceptLinkCreationRequest,
)

router = APIRouter()


@router.get("/knowledge/concepts")
def get_concepts(db: Session = Depends(get_db)) -> list[Concept]:
    return db_knowledge.get_all_concepts(db)


@router.get("/knowledge/concepts/{concept_id}")
def get_concept(
    concept_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> Concept | None:
    return db_knowledge.get_concept_by_id(db, concept_id)


@router.get("/knowledge/concepts/{concept_id}/detail")
def get_concept_detail(
    concept_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> ConceptDetail:
    result = db_knowledge.get_concept_detail(db, concept_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Concept not found.")
    return result


@router.post("/knowledge/concepts")
def create_concept(
    concept: ConceptCreationRequest,
    db: Session = Depends(get_db),
) -> Concept:
    return db_knowledge.create_concept(db, concept)


@router.post("/knowledge/concept-links", status_code=status.HTTP_201_CREATED)
def create_concept_link(
    concept_link: ConceptLinkCreationRequest,
    db: Session = Depends(get_db),
) -> ConceptLink:
    result = db_knowledge.create_concept_link(db, concept_link)
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
) -> Comment:
    result = db_knowledge.create_comment(db, comment.commentable_id, comment)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commentable record or creator was not found.",
        )
    return result