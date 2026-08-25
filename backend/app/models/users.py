from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import UUIDBase

if TYPE_CHECKING:
    from app.models.knowledge import Commentable, CommentModel  # noqa: F401


class UserModel(UUIDBase):
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    is_curator: Mapped[bool] = mapped_column(Boolean, default=False)
    commentables: Mapped[list["Commentable"]] = relationship(
        back_populates="creator",
        foreign_keys="Commentable.creator_id",
        cascade="all, delete-orphan",
    )
    user_comments: Mapped[list["CommentModel"]] = relationship(
        back_populates="creator",
        foreign_keys="CommentModel.creator_id",
        cascade="all, delete-orphan",
    )