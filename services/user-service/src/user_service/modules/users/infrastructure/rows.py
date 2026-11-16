from typing import TypedDict
from uuid import UUID


class UserRow(TypedDict):
    id: UUID
    name: str
    email: str
