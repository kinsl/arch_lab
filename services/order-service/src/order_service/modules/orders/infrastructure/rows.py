from typing import TypedDict
from uuid import UUID


class OrderRow(TypedDict):
    id: UUID
    user_id: UUID
    product: str
    quantity: int
    email: str
    notification_status: str
