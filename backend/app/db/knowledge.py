import uuid

from sqlalchemy.orm import Session

from app.models.knowledge import (
    Commentable,
    CommentModel,
    ConceptLinkModel,
    ConceptModel,
)
from app.models.users import UserModel
from app.schemas.knowledge import (
    Comment,
    CommentCreationRequest,
    Concept,
    ConceptComment,
    ConceptCreationRequest,
    ConceptCreator,
    ConceptDetail,
    ConceptLink,
    ConceptLinkCreationRequest,
    LinkedConcept,
)
from app.types import fed_id


def get_all_concepts(db: Session) -> list[Concept]:
    """Retrieve all concepts from the database."""
    concepts = db.query(ConceptModel).all()
    return [
        Concept(
            id=concept.id,
            creator_id=concept.creator_id,
            name=concept.name,
            description=concept.description,
        )
        for concept in concepts
    ]


def get_concept_by_id(db: Session, concept_id: uuid.UUID) -> Concept | None:
    """Retrieve a concept by its ID from the database."""
    concept_model = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if concept_model:
        return Concept(
            id=concept_model.id,
            creator_id=concept_model.creator_id,
            name=concept_model.name,
            description=concept_model.description,
        )
    return None


def get_concept_detail(db: Session, concept_id: uuid.UUID) -> ConceptDetail | None:
    """Retrieve a concept along with its creator, links, and comments."""
    concept_model = db.query(ConceptModel).filter(ConceptModel.id == concept_id).first()
    if not concept_model:
        return None

    creator = db.get(UserModel, concept_model.creator_id)
    assert creator is not None  # enforced by the creator_id foreign key

    linked_concepts = [link.target_concept for link in concept_model.outgoing_links] + [
        link.source_concept for link in concept_model.incoming_links
    ]

    comments = db.query(CommentModel).filter(CommentModel.commentable_id == concept_id).all()

    return ConceptDetail(
        id=concept_model.id,
        name=concept_model.name,
        description=concept_model.description,
        creator=ConceptCreator(id=creator.id, username=creator.username),
        linked_concepts=[LinkedConcept(id=c.id, name=c.name) for c in linked_concepts],
        comments=[
            ConceptComment(
                id=comment.id,
                content=comment.content,
                creator=ConceptCreator(
                    id=comment.creator.id, username=comment.creator.username
                ),
            )
            for comment in comments
        ],
    )


def create_concept(db: Session, creator_id: fed_id, concept: ConceptCreationRequest) -> Concept:
    """Create a new concept in the database."""
    new_concept = ConceptModel(
        creator_id=creator_id,
        name=concept.name,
        description=concept.description,
    )
    db.add(new_concept)
    db.commit()
    db.refresh(new_concept)
    return Concept(
        id=new_concept.id,
        creator_id=new_concept.creator_id,
        name=new_concept.name,
        description=new_concept.description,
    )


def get_link_if_exists(db: Session, source_concept_id: fed_id, target_concept_id: fed_id) -> bool:
    """Check if a link already exists between two concepts."""
    link = (
        db.query(ConceptLinkModel)
        .filter(
            ConceptLinkModel.source_concept_id == source_concept_id,
            ConceptLinkModel.target_concept_id == target_concept_id,
        )
        .first()
    )
    return link is not None

def create_concept_link(
    db: Session, creator_id: fed_id, concept_link: ConceptLinkCreationRequest
) -> ConceptLink:
    existing = get_link_if_exists(db, concept_link.source_concept_id, concept_link.target_concept_id)
    if existing:
        raise ValueError("Concept link already exists.")
    
    """Link two existing concepts."""
    source = db.get(ConceptModel, concept_link.source_concept_id)
    if not source:
        raise ValueError(f"Source concept {concept_link.source_concept_id} not found.")
    target = db.get(ConceptModel, concept_link.target_concept_id)
    if not target:
        raise ValueError(f"Target concept {concept_link.target_concept_id} not found.")
    creator = db.get(UserModel, creator_id)
    if not creator:
        raise ValueError(f"Creator {creator_id} not found.")

    new_link = ConceptLinkModel(
        creator_id=creator_id,
        source_concept_id=concept_link.source_concept_id,
        target_concept_id=concept_link.target_concept_id,
        connection=concept_link.connection,
    )
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return ConceptLink(
        id=new_link.id,
        creator_id=new_link.creator_id,
        source_concept_id=new_link.source_concept_id,
        target_concept_id=new_link.target_concept_id,
        connection=new_link.connection,
    )


def get_link_by_id(db: Session, link_id: fed_id) -> ConceptLink | None:
    """Retrieve a concept link by its ID."""
    link_model = db.query(ConceptLinkModel).filter(ConceptLinkModel.id == link_id).first()
    if not link_model:
        return None
    return ConceptLink(
        id=link_model.id,
        creator_id=link_model.creator_id,
        source_concept_id=link_model.source_concept_id,
        target_concept_id=link_model.target_concept_id,
        connection=link_model.connection,
    )


def create_comment(
    db: Session, commentable_id: fed_id, creator_id: fed_id, comment: CommentCreationRequest
) -> Comment | None:
    """Add a comment to an existing concept or concept link."""
    commentable = db.get(Commentable, commentable_id)
    creator = db.get(UserModel, creator_id)
    if not commentable or not creator:
        return None

    new_comment = CommentModel(
        commentable_id=commentable_id,
        creator_id=creator_id,
        content=comment.content,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return Comment(
        id=new_comment.id,
        commentable_id=new_comment.commentable_id,
        creator_id=new_comment.creator_id,
        content=new_comment.content,
    )


def update_concept(db: Session, concept: Concept) -> Concept | None:
    """Update an existing concept in the database."""
    concept_model = db.query(ConceptModel).filter(ConceptModel.id == concept.id).first()
    if not concept_model:
        return None

    if concept.name is not None:
        concept_model.name = concept.name
    if concept.description is not None:
        concept_model.description = concept.description

    db.commit()
    db.refresh(concept_model)
    return Concept(
        id=concept_model.id,
        creator_id=concept_model.creator_id,
        name=concept_model.name,
        description=concept_model.description,
    )