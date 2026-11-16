from dataclasses import dataclass
from uuid import UUID

from notification_service.modules.notifications.domain.entities.notification import Notification


@dataclass(frozen=True, slots=True)
class CreateNotificationResult:
    notification: Notification
    created: bool


@dataclass(frozen=True, slots=True)
class CreateNotificationDTO:
    order_id: UUID
    email: str
    message: str


@dataclass(frozen=True, slots=True)
class UpdateNotificationDTO:
    email: str
    message: str
