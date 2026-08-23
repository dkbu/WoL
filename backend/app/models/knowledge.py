
import uuid

from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, Relationship, mapped_column, relationship

from app.models.base import UUIDBase


class CommentableModel(UUIDBase):
    """Base class for all SQLAlchemy models that can be commented on."""

    __abstract__ = True

    comments: Relationship["CommentModel"] = relationship(  # noqa: UP037
        "CommentModel",
        back_populates="commentable",
        cascade="all, delete-orphan",
    )
    

class ConceptModel(CommentableModel):
    """SQLAlchemy model for concept."""

    name: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=True,
    )


class ConceptLinkModel(CommentableModel):
    """SQLAlchemy model for concept link."""

    __table_args__ = (
        UniqueConstraint(
            "source_concept_id",
            "target_concept_id",
            name="uq_concept_link_source_target",
        ),
    )

    source_concept_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=False,
        nullable=False,
    )
    target_concept_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=False,
        nullable=False,
    )


class CommentModel(UUIDBase):
    """SQLAlchemy model for comment."""

    content: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=False,
    )
    commentable_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=False,
        nullable=False,
    )
    commentable_type: Mapped[str] = mapped_column(
        String(255),
        unique=False,
        nullable=False,
    )

    commentable: Mapped[CommentableModel] = relationship(
        "CommentableModel",
        back_populates="comments",
    )

