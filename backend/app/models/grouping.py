from app.models.base import UUIDBase
from app.schemas.knowledge import Concept
from app.schemas.users import User
from sqlalchemy.orm import Mapped, relationship


class Grouping(UUIDBase):
    pass


class ConceptGrouping(UUIDBase):
    __tablename__ = "concept_groupings"

    name: Mapped[str]

    # how to display the grouping in the UI
    style: Mapped[str]

    concepts: Mapped[list["Concept"]] = relationship(
        back_populates="groupings",
        foreign_keys="ConceptGrouping.id"
    )


# A grouping of concepts, potentially created by multiple users, that share a common theme
class ConceptPool(ConceptGrouping):
    __tablename__ = "concept_pools"

    @staticmethod
    def pool_style() -> str:
        return "pool"

    maintainers: Mapped[list["User"]] = relationship(
        back_populates="pools",
        foreign_keys="ConceptPool.id"
    )


# A grouping of concepts that a user is inspired by
class ConceptLibrary(ConceptGrouping):
    __tablename__ = "concept_libraries"

    @staticmethod
    def library_style() -> str:
        return "library"

    owner: Mapped["User"] = relationship(
        back_populates="libraries",
        foreign_keys="ConceptLibrary.id"
    )