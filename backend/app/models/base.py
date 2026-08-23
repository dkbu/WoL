from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Relationship,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.

    All entities that will be externally addressable use UUID primary keys
    to support future federation.
    """



def new_uuid() -> uuid.UUID:
    """Generate a new UUID for use as a primary key."""
    return uuid.uuid4()


class UUIDBase(Base):
    """Base class for all SQLAlchemy models that use UUID primary keys."""

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=new_uuid,
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        unique=False,
        nullable=False,
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        unique=False,
        nullable=False,
        default=datetime.now, 
        onupdate=datetime.now,
    )


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



