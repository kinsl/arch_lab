from uuid import UUID

from notification_service.modules.notifications.domain.entities.notification import Notification
from notification_service.modules.notifications.infrastructure.repositories.notifications_repository import (
    NotificationRepository,
)


class ListNotificationsUseCase:
    def __init__(self, repository: NotificationRepository) -> None:
        self._repository = repository

    async def execute(self, *, limit: int, offset: int, order_id: UUID | None = None) -> list[Notification]:
        return await self._repository.list(limit=limit, offset=offset, order_id=order_id)
