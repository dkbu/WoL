from typing import TYPE_CHECKING
from uuid import UUID as PyUUID

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import UUIDBase

if TYPE_CHECKING:
    from app.models.knowledge import Commentable, CommentModel  # noqa: F401


class UserModel(UUIDBase):
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_curator: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
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
    following: Mapped[list["FollowModel"]] = relationship(
        back_populates="follower",
        foreign_keys="FollowModel.follower_id",
        cascade="all, delete-orphan",
    )
    followers: Mapped[list["FollowModel"]] = relationship(
        back_populates="followed",
        foreign_keys="FollowModel.followed_id",
        cascade="all, delete-orphan",
    )


class FollowModel(UUIDBase):
    """One user (follower) following another (followed)."""

    __tablename__ = "follows"

    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="uq_follow_follower_followed"),
    )

    follower_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    followed_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    follower: Mapped["UserModel"] = relationship(
        back_populates="following", foreign_keys=[follower_id]
    )
    followed: Mapped["UserModel"] = relationship(
        back_populates="followers", foreign_keys=[followed_id]
    )