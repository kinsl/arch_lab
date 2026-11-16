from notification_service.modules.notifications.domain.entities.notification import Notification
from notification_service.modules.notifications.infrastructure.rows import NotificationRow


class NotificationMapper:
    @staticmethod
    def to_entity(row: NotificationRow) -> Notification:
        return Notification(
            id=row["id"],
            order_id=row["order_id"],
            email=row["email"],
            message=row["message"],
        )
