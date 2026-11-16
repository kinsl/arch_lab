import logging

from order_service.modules.orders.domain.entities.order import Order
from order_service.modules.orders.domain.errors import DependencyUnavailableError
from order_service.modules.orders.domain.notification_status import NotificationStatus
from order_service.modules.orders.infrastructure.clients.service_clients import HttpNotificationGateway
from order_service.modules.orders.infrastructure.repositories.orders_repository import OrderRepository

logger = logging.getLogger(__name__)


class OrderNotificationService:
    def __init__(self, repository: OrderRepository, notifications: HttpNotificationGateway) -> None:
        self._repository = repository
        self._notifications = notifications

    async def deliver(self, order: Order) -> Order:
        try:
            await self._notifications.send(order.id, order.email)
        except DependencyUnavailableError:
            logger.warning("Notification pending for order %s", order.id)
            return order
        return await self._repository.set_notification_status(order.id, NotificationStatus.SENT)
