from order_service.modules.orders.application.dto import CreateOrderDTO
from order_service.modules.orders.application.services.order_notification_service import OrderNotificationService
from order_service.modules.orders.domain.entities.order import NewOrder, Order
from order_service.modules.orders.infrastructure.clients.service_clients import HttpUserGateway
from order_service.modules.orders.infrastructure.repositories.orders_repository import OrderRepository


class CreateOrderUseCase:
    def __init__(self, repository: OrderRepository, users: HttpUserGateway, delivery: OrderNotificationService) -> None:
        self._repository = repository
        self._users = users
        self._delivery = delivery

    async def execute(self, data: CreateOrderDTO) -> Order:
        email = await self._users.get_email(data.user_id)
        order = await self._repository.add(
            NewOrder(
                user_id=data.user_id,
                product=data.product,
                quantity=data.quantity,
                email=email,
            )
        )
        return await self._delivery.deliver(order)
