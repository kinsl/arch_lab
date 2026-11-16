from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncConnection

from notification_service.modules.notifications.application.use_cases.create_notification_use_case import (
    CreateNotificationUseCase,
)
from notification_service.modules.notifications.application.use_cases.delete_notification_use_case import (
    DeleteNotificationUseCase,
)
from notification_service.modules.notifications.application.use_cases.get_notification_use_case import (
    GetNotificationUseCase,
)
from notification_service.modules.notifications.application.use_cases.list_notifications_use_case import (
    ListNotificationsUseCase,
)
from notification_service.modules.notifications.application.use_cases.update_notification_use_case import (
    UpdateNotificationUseCase,
)
from notification_service.modules.notifications.infrastructure.repositories.notifications_repository import (
    NotificationRepository,
)
from notification_service.modules.notifications.infrastructure.senders.logging_notification_sender import (
    LoggingNotificationSender,
)


class NotificationProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def repository(self, connection: AsyncConnection) -> NotificationRepository:
        return NotificationRepository(connection)

    @provide
    def sender(self) -> LoggingNotificationSender:
        return LoggingNotificationSender()

    @provide
    def create_notification(
        self, repository: NotificationRepository, sender: LoggingNotificationSender
    ) -> CreateNotificationUseCase:
        return CreateNotificationUseCase(repository, sender)

    @provide
    def get_notification(self, repository: NotificationRepository) -> GetNotificationUseCase:
        return GetNotificationUseCase(repository)

    @provide
    def list_notifications(self, repository: NotificationRepository) -> ListNotificationsUseCase:
        return ListNotificationsUseCase(repository)

    @provide
    def update_notification(self, repository: NotificationRepository) -> UpdateNotificationUseCase:
        return UpdateNotificationUseCase(repository)

    @provide
    def delete_notification(self, repository: NotificationRepository) -> DeleteNotificationUseCase:
        return DeleteNotificationUseCase(repository)
