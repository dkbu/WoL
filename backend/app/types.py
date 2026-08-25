from uuid import UUID

# A single canonical UUID type: Pydantic coerces incoming str/UUID input to a
# real uuid.UUID and serializes it back to a string in JSON responses. Using a
# plain `str | UUID` union here previously let JSON string input pass through
# as `str`, which broke SQLAlchemy UUID columns expecting a real UUID object.
fed_id = UUID