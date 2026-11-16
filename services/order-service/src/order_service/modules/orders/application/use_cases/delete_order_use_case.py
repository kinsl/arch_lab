from uuid import UUID

from order_service.modules.orders.infrastructure.repositories.orders_repository import OrderRepository


class DeleteOrderUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    async def execute(self, item_id: UUID) -> None:
        await self._repository.delete(item_id)
