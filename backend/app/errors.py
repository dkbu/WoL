from app.types import fed_id


class NotFoundError(Exception):
    def __init__(self, what: str):
        super().__init__(f"{what} not found.")


class ConceptNotFoundError(NotFoundError):
    def __init__(self, concept_id: fed_id):
        super().__init__(f"Concept {concept_id} not found.")


class LibraryNotFoundError(NotFoundError):
    def __init__(self, library_id: fed_id):
        super().__init__(f"Library {library_id} not found.")


class ForbiddenError(Exception):
    def __init__(self, user: fed_id, what: str):
        super().__init__(f"Forbidden: {user} cannot access {what}.")
