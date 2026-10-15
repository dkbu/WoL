from pydantic import BaseModel

from app.types import fed_id


class ChangeConceptRequest(BaseModel):
    concept_id: fed_id
    library_id: fed_id
