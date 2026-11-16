from uuid import UUID

from order_service.modules.orders.domain.entities.order import Order
from order_service.modules.orders.infrastructure.repositories.orders_repository import OrderRepository


class GetOrderUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    async def execute(self, item_id: UUID) -> Order:
        return await self._repository.get(item_id)
