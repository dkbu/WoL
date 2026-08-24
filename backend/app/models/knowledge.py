
import uuid

from sqlalchemy import CheckConstraint, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import UUIDBase


class ConceptModel(UUIDBase):
    """SQLAlchemy model for concept."""

    __tablename__ = "concepts"

    comments: Mapped[list["CommentModel"]] = relationship(
        back_populates="concept",
        foreign_keys="CommentModel.concept_id",
        cascade="all, delete-orphan",
    )

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


class ConceptLinkModel(UUIDBase):
    """SQLAlchemy model for concept link."""

    __tablename__ = "concept_links"

    comments: Mapped[list["CommentModel"]] = relationship(
        back_populates="link",
        foreign_keys="CommentModel.link_id",
        cascade="all, delete-orphan",
    )

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
    concept_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conceptmodel.id"),
        unique=False,
        nullable=True,
    )
    link_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conceptlinkmodel.id"),
        unique=False,
        nullable=True,
    )
    concept: Mapped[ConceptModel | None] = relationship(
        back_populates="comments",
        foreign_keys=[concept_id],
    )
    link: Mapped[ConceptLinkModel | None] = relationship(
        back_populates="comments",
        foreign_keys=[link_id],
    )

