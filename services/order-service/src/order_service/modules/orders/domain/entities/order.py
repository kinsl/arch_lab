from dataclasses import dataclass
from uuid import UUID

from order_service.modules.orders.domain.notification_status import NotificationStatus


@dataclass(frozen=True, slots=True)
class Order:
    id: UUID
    user_id: UUID
    product: str
    quantity: int
    email: str
    notification_status: NotificationStatus


@dataclass(frozen=True, slots=True)
class NewOrder:
    user_id: UUID
    product: str
    quantity: int
    email: str
    notification_status: NotificationStatus = NotificationStatus.PENDING
