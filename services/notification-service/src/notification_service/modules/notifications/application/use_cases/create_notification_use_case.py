from notification_service.modules.notifications.application.dto import CreateNotificationDTO
from notification_service.modules.notifications.domain.entities.notification import Notification
from notification_service.modules.notifications.infrastructure.repositories.notifications_repository import (
    NotificationRepository,
)
from notification_service.modules.notifications.infrastructure.senders.logging_notification_sender import (
    LoggingNotificationSender,
)


class CreateNotificationUseCase:
    def __init__(self, repository: NotificationRepository, sender: LoggingNotificationSender) -> None:
        self._repository = repository
        self._sender = sender

    async def execute(self, data: CreateNotificationDTO) -> Notification:
        result = await self._repository.add(data)
        if result.created:
            self._sender.send(result.notification)
        return result.notification
