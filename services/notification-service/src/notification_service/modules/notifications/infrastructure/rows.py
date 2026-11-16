from typing import TypedDict
from uuid import UUID


class NotificationRow(TypedDict):
    id: UUID
    order_id: UUID
    email: str
    message: str
