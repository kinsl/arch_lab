from order_service.modules.orders.domain.entities.order import Order
from order_service.modules.orders.domain.notification_status import NotificationStatus
from order_service.modules.orders.infrastructure.rows import OrderRow


class OrderMapper:
    @staticmethod
    def to_entity(row: OrderRow) -> Order:
        return Order(
            id=row["id"],
            user_id=row["user_id"],
            product=row["product"],
            quantity=row["quantity"],
            email=row["email"],
            notification_status=NotificationStatus(row["notification_status"]),
        )
