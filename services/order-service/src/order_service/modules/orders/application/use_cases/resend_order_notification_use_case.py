from uuid import UUID

from order_service.modules.orders.application.services.order_notification_service import OrderNotificationService
from order_service.modules.orders.domain.entities.order import Order
from order_service.modules.orders.infrastructure.repositories.orders_repository import OrderRepository


class ResendOrderNotificationUseCase:
    def __init__(self, repository: OrderRepository, delivery: OrderNotificationService) -> None:
        self._repository = repository
        self._delivery = delivery

    async def execute(self, item_id: UUID) -> Order:
        order = await self._repository.get(item_id)
        return await self._delivery.deliver(order)
