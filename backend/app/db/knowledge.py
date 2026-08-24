import uuid

from sqlalchemy.orm import Session

from app.models.knowledge import ConceptModel
from app.schemas.knowledge import Concept


def get_all_concepts(db: Session) -> list[Concept]:
    """Retrieve all concepts from the database."""
    concepts = db.query(ConceptModel).all()
    return [Concept(id=c.id, name=c.name, description=c.description) for c in concepts]


def get_concept_by_id(db: Session, concept_id: uuid.UUID) -> Concept | None:
    """Retrieve a concept by its ID from the database."""
    concept_model = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if concept_model:
        return Concept(id=concept_model.id, name=concept_model.name, description=concept_model.description)
    return None


def create_concept(db: Session, concept: Concept) -> Concept:
    """Create a new concept in the database."""
    new_concept = ConceptModel(name=concept.name, description=concept.description)
    db.add(new_concept)
    db.commit()
    db.refresh(new_concept)
    return Concept(id=new_concept.id, name=new_concept.name, description=new_concept.description)


def update_concept(db: Session, concept_id: uuid.UUID, name: str | None = None, description: str | None = None) -> Concept | None:
    """Update an existing concept in the database."""
    concept_model = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if not concept_model:
        return None

    if name is not None:
        concept_model.name = name
    if description is not None:
        concept_model.description = description

    db.commit()
    db.refresh(concept_model)
    return Concept(id=concept_model.id, name=concept_model.name, description=concept_model.description)