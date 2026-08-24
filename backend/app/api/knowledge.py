import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.db import knowledge as db_knowledge
from app.schemas.knowledge import Concept, ConceptCreationRequest

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


@router.post("/knowledge/concepts")
def create_concept(
    concept: ConceptCreationRequest,
    db: Session = Depends(get_db),
) -> Concept:
    return db_knowledge.create_concept(db, concept)