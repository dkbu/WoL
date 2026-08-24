
import uuid

from sqlalchemy import CheckConstraint, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import UUIDBase


class Commentable(UUIDBase):
    """Base class for models that can have comments."""

    __abstract__ = True

    comments: Mapped[list["CommentModel"]] = relationship(
        back_populates="concept",
        foreign_keys="CommentModel.concept_id",
        cascade="all, delete-orphan",
    )


class ConceptModel(Commentable):
    """SQLAlchemy model for concept."""

    __tablename__ = "concepts"

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


class ConceptLinkModel(Commentable):
    """SQLAlchemy model for concept link."""

    __tablename__ = "concept_links"

    # comments relationship inherited from Commentable

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

    __tablename__ = "comments"

    __table_args__ = (
        CheckConstraint(
            "(concept_id IS NOT NULL) <> (link_id IS NOT NULL)",
            name="ck_comment_exactly_one_target",
        ),
    )

    content: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=False,
    )
    commentable_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("concepts.id"),
        unique=False,
        nullable=True,
    )
    commentable: Mapped[ConceptModel | None] = relationship(
        back_populates="comments",
        foreign_keys=[commentable_id],
    )

