from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
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
