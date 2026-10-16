from sqlalchemy.orm import Mapped, relationship

from app.models.base import UUIDBase
from app.schemas.users import User
from app.types import fed_id


class ConceptGrouping(UUIDBase):
    __abstract__ = True

    name: Mapped[str]

    # how to display the grouping in the UI
    style: Mapped[str]

    is_public: Mapped[bool]


# A grouping of concepts, potentially created by multiple users,
# that share a common theme
# if a pool is public, any user may add concepts to it
class ConceptPool(ConceptGrouping):
    __tablename__ = "concept_pools"

    @staticmethod
    def pool_style() -> str:
        return "pool"

    maintainers: Mapped[list["User"]] = relationship(
        back_populates="pools", foreign_keys="ConceptPool.id"
    )


# A grouping of concepts that a user is inspired by
# if a library is public, any user may view it
class ConceptLibrary(ConceptGrouping):
    __tablename__ = "concept_libraries"

    @staticmethod
    def library_style() -> str:
        return "library"

    owner: Mapped["User"] = relationship(
        back_populates="libraries", foreign_keys="ConceptLibrary.id"
    )
    owner_id: Mapped[fed_id]
