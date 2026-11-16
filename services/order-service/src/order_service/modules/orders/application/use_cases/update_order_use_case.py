from uuid import UUID

from order_service.modules.orders.application.dto import UpdateOrderDTO
from order_service.modules.orders.domain.entities.order import Order
from order_service.modules.orders.infrastructure.repositories.orders_repository import OrderRepository


class UpdateOrderUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    async def execute(self, item_id: UUID, data: UpdateOrderDTO) -> Order:
        return await self._repository.update(item_id, data)
