from sqlalchemy.orm import Query, Session

from app.db.knowledge import get_concept_by_id
from app.errors import ConceptNotFoundError, LibraryNotFoundError
from app.models.grouping import ConceptLibrary, ConceptPool
from app.schemas.users import User
from app.types import fed_id


def libraries_user_can_access(
    query: Query[ConceptLibrary], current_user: User
) -> Query[ConceptLibrary]:
    return query.filter(
        (ConceptLibrary.is_public) | (ConceptLibrary.owner_id == current_user.id)
    )


def get_pool_by_id(db: Session, pool_id: fed_id) -> ConceptPool | None:
    return db.query(ConceptPool).filter(ConceptPool.id == pool_id).first()


def get_library_by_id(
    db: Session, library_id: fed_id, current_user: User
) -> ConceptLibrary | None:
    return (
        libraries_user_can_access(db.query(ConceptLibrary), current_user)
        .filter(ConceptLibrary.id == library_id)
        .first()
    )


def add_concept_to_library(
    db: Session, library_id: fed_id, concept_id: fed_id, current_user: User
) -> None:
    library = get_library_by_id(db, library_id, current_user)
    if not library:
        raise LibraryNotFoundError(library_id)
    concept = get_concept_by_id(db, concept_id)
    if not concept:
        raise ConceptNotFoundError(concept_id)
    library.concepts.append(concept)
    db.commit()


def remove_concept_from_library(
    db: Session, library_id: fed_id, concept_id: fed_id, current_user: User
) -> None:
    library = get_library_by_id(db, library_id, current_user)
    if not library:
        raise LibraryNotFoundError(library_id)
    concept = get_concept_by_id(db, concept_id)
    if not concept:
        raise ConceptNotFoundError(concept_id)
    if concept in library.concepts:
        library.concepts.remove(concept)
        db.commit()
