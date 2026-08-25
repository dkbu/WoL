"""Seed script: loads museum.db with three demo users, six concepts, and cross comments.

Run via `uv run seed` from backend/.
"""

from __future__ import annotations

from app.db.session import SessionLocal
from app.models.knowledge import CommentModel, ConceptModel
from app.models.users import UserModel

USERNAMES = ["steve", "robin", "eddie"]


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(UserModel).filter(UserModel.username.in_(USERNAMES)).first():
            print("Seed data already present, skipping.")
            return

        users = {name: UserModel(username=name, is_curator=False) for name in USERNAMES}
        db.add_all(users.values())
        db.flush()

        concepts_by_creator: dict[str, list[ConceptModel]] = {name: [] for name in USERNAMES}
        for name, user in users.items():
            for i in range(1, 3):
                concept = ConceptModel(
                    creator_id=user.id,
                    name=f"{name.capitalize()}'s concept {i}",
                    description=f"A dummy concept created by {name}.",
                )
                db.add(concept)
                concepts_by_creator[name].append(concept)
        db.flush()

        for name, user in users.items():
            for other_name, concepts in concepts_by_creator.items():
                if other_name == name:
                    continue
                for concept in concepts:
                    db.add(
                        CommentModel(
                            commentable_id=concept.id,
                            creator_id=user.id,
                            content=f"{name.capitalize()} commented on '{concept.name}'.",
                        )
                    )

        db.commit()
        print("Seeded 3 users, 6 concepts, and 12 comments.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
