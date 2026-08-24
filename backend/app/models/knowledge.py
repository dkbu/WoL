
import uuid
from typing import ClassVar

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import UUIDBase


class Commentable(UUIDBase):
    """Base class for models that can have comments."""

    __tablename__ = "commentables"

    type: Mapped[str] = mapped_column(String(50), nullable=False)

    comments: Mapped[list["CommentModel"]] = relationship(
        back_populates="commentable",
        foreign_keys="CommentModel.commentable_id",
        cascade="all, delete-orphan",
    )

    __mapper_args__: ClassVar[dict[str, object]] = {  # type: ignore[reportIncompatibleVariableOverride]
        "polymorphic_on": type,
        "polymorphic_identity": "commentable",
    }


class ConceptModel(Commentable):
    """SQLAlchemy model for concept."""

    __tablename__ = "concepts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("commentables.id"), primary_key=True
    )

    __mapper_args__: ClassVar[dict[str, object]] = {"polymorphic_identity": "concept"}

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

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("commentables.id"), primary_key=True
    )

    __mapper_args__: ClassVar[dict[str, object]] = {"polymorphic_identity": "concept_link"}

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

    content: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=False,
    )
    commentable_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("commentables.id"),
        unique=False,
        nullable=False,
    )
    commentable: Mapped[Commentable] = relationship(
        back_populates="comments",
        foreign_keys=[commentable_id],
    )

