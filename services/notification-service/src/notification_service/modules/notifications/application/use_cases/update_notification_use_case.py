from uuid import UUID

from notification_service.modules.notifications.application.dto import UpdateNotificationDTO
from notification_service.modules.notifications.domain.entities.notification import Notification
from notification_service.modules.notifications.infrastructure.repositories.notifications_repository import (
    NotificationRepository,
)


class UpdateNotificationUseCase:
    def __init__(self, repository: NotificationRepository) -> None:
        self._repository = repository

    async def execute(self, item_id: UUID, data: UpdateNotificationDTO) -> Notification:
        return await self._repository.update(item_id, data)
