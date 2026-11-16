from order_service.modules.orders.domain.entities.order import Order
from order_service.modules.orders.infrastructure.repositories.orders_repository import OrderRepository


class ListOrdersUseCase:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    async def execute(self, *, limit: int, offset: int) -> list[Order]:
        return await self._repository.list(limit=limit, offset=offset)
