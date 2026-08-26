"""Seed script: loads museum.db with three demo users, six concepts, and cross comments.

Run via `uv run seed` from backend/.
"""

from __future__ import annotations

from app.db.session import SessionLocal
from app.models.knowledge import CommentModel, ConceptModel
from app.models.users import UserModel
from app.security import hash_password

USERNAMES = ["steve", "robin", "eddie"]
SEED_PASSWORD = "password123"  # noqa: S105 - demo-only seed data, not a real secret

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"  # noqa: S105 - local dev only; change before deploying anywhere real


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(UserModel).filter(UserModel.username.in_(USERNAMES)).first():
            print("Seed data already present, skipping.")
            return

        if not db.query(UserModel).filter(UserModel.username == ADMIN_USERNAME).first():
            db.add(
                UserModel(
                    username=ADMIN_USERNAME,
                    password_hash=hash_password(ADMIN_PASSWORD),
                    is_curator=True,
                    is_admin=True,
                )
            )

        users = {
            name: UserModel(
                username=name,
                password_hash=hash_password(SEED_PASSWORD),
                is_curator=True,
            )
            for name in USERNAMES
        }
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
        print("Seeded 1 admin user, 3 demo users, 6 concepts, and 12 comments.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
