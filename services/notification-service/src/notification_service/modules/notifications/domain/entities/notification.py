from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Notification:
    id: UUID
    order_id: UUID
    email: str
    message: str
