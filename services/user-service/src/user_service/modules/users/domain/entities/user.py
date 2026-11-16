from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class User:
    id: UUID
    name: str
    email: str
