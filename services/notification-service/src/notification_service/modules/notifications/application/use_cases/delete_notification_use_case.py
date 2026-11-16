from uuid import UUID

from notification_service.modules.notifications.infrastructure.repositories.notifications_repository import (
    NotificationRepository,
)


class DeleteNotificationUseCase:
    def __init__(self, repository: NotificationRepository) -> None:
        self._repository = repository

    async def execute(self, item_id: UUID) -> None:
        await self._repository.delete(item_id)
