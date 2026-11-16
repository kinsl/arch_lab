import logging

from notification_service.modules.notifications.domain.entities.notification import Notification

logger = logging.getLogger(__name__)


class LoggingNotificationSender:
    def send(self, notification: Notification) -> None:
        logger.info(
            "EMAIL STUB to=%s order=%s message=%s",
            notification.email,
            notification.order_id,
            notification.message,
        )
