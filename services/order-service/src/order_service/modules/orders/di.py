from dishka import Provider, Scope, provide
from httpx2 import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection

from order_service.app.config import Config
from order_service.modules.orders.application.services.order_notification_service import OrderNotificationService
from order_service.modules.orders.application.use_cases.create_order_use_case import CreateOrderUseCase
from order_service.modules.orders.application.use_cases.delete_order_use_case import DeleteOrderUseCase
from order_service.modules.orders.application.use_cases.get_order_use_case import GetOrderUseCase
from order_service.modules.orders.application.use_cases.list_orders_use_case import ListOrdersUseCase
from order_service.modules.orders.application.use_cases.resend_order_notification_use_case import (
    ResendOrderNotificationUseCase,
)
from order_service.modules.orders.application.use_cases.update_order_use_case import UpdateOrderUseCase
from order_service.modules.orders.infrastructure.clients.service_clients import HttpNotificationGateway, HttpUserGateway
from order_service.modules.orders.infrastructure.repositories.orders_repository import OrderRepository


class OrderProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def repository(self, connection: AsyncConnection) -> OrderRepository:
        return OrderRepository(connection)

    @provide
    def create_order(
        self, repository: OrderRepository, users: HttpUserGateway, delivery: OrderNotificationService
    ) -> CreateOrderUseCase:
        return CreateOrderUseCase(repository, users, delivery)

    @provide
    def get_order(self, repository: OrderRepository) -> GetOrderUseCase:
        return GetOrderUseCase(repository)

    @provide
    def list_orders(self, repository: OrderRepository) -> ListOrdersUseCase:
        return ListOrdersUseCase(repository)

    @provide
    def update_order(self, repository: OrderRepository) -> UpdateOrderUseCase:
        return UpdateOrderUseCase(repository)

    @provide
    def delete_order(self, repository: OrderRepository) -> DeleteOrderUseCase:
        return DeleteOrderUseCase(repository)

    @provide
    def resend_order_notification(
        self, repository: OrderRepository, delivery: OrderNotificationService
    ) -> ResendOrderNotificationUseCase:
        return ResendOrderNotificationUseCase(repository, delivery)

    @provide
    def users(self, client: AsyncClient, config: Config) -> HttpUserGateway:
        return HttpUserGateway(client, config.user_service_url)

    @provide
    def notifications(self, client: AsyncClient, config: Config) -> HttpNotificationGateway:
        return HttpNotificationGateway(client, config.notification_service_url)

    @provide
    def delivery(self, repository: OrderRepository, notifications: HttpNotificationGateway) -> OrderNotificationService:
        return OrderNotificationService(repository, notifications)
