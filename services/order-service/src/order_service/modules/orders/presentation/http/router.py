from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, Response

from order_service.modules.orders.application.use_cases.create_order_use_case import CreateOrderUseCase
from order_service.modules.orders.application.use_cases.delete_order_use_case import DeleteOrderUseCase
from order_service.modules.orders.application.use_cases.get_order_use_case import GetOrderUseCase
from order_service.modules.orders.application.use_cases.list_orders_use_case import ListOrdersUseCase
from order_service.modules.orders.application.use_cases.resend_order_notification_use_case import (
    ResendOrderNotificationUseCase,
)
from order_service.modules.orders.application.use_cases.update_order_use_case import UpdateOrderUseCase
from order_service.modules.orders.domain.entities.order import Order
from order_service.modules.orders.presentation.http.schemas import (
    CreateOrderBody,
    OrderResponse,
    UpdateOrderBody,
)

router = APIRouter(prefix="/orders", tags=["orders"], route_class=DishkaRoute)


@router.post("", response_model=OrderResponse, status_code=201)
async def create(body: CreateOrderBody, use_case: FromDishka[CreateOrderUseCase]) -> Order:
    return await use_case.execute(body.to_dto())


@router.get("", response_model=list[OrderResponse])
async def list_items(
    use_case: FromDishka[ListOrdersUseCase],
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Order]:
    return await use_case.execute(limit=limit, offset=offset)


@router.get("/{item_id}", response_model=OrderResponse)
async def get(item_id: UUID, use_case: FromDishka[GetOrderUseCase]) -> Order:
    return await use_case.execute(item_id)


@router.put("/{item_id}", response_model=OrderResponse)
async def update(item_id: UUID, body: UpdateOrderBody, use_case: FromDishka[UpdateOrderUseCase]) -> Order:
    return await use_case.execute(item_id, body.to_dto())


@router.delete("/{item_id}", status_code=204)
async def delete(item_id: UUID, use_case: FromDishka[DeleteOrderUseCase]) -> Response:
    await use_case.execute(item_id)
    return Response(status_code=204)


@router.post("/{item_id}/notification", response_model=OrderResponse)
async def resend(item_id: UUID, use_case: FromDishka[ResendOrderNotificationUseCase]) -> Order:
    return await use_case.execute(item_id)
