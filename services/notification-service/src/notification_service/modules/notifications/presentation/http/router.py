from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, Response

from notification_service.modules.notifications.application.use_cases.create_notification_use_case import (
    CreateNotificationUseCase,
)
from notification_service.modules.notifications.application.use_cases.delete_notification_use_case import (
    DeleteNotificationUseCase,
)
from notification_service.modules.notifications.application.use_cases.get_notification_use_case import (
    GetNotificationUseCase,
)
from notification_service.modules.notifications.application.use_cases.list_notifications_use_case import (
    ListNotificationsUseCase,
)
from notification_service.modules.notifications.application.use_cases.update_notification_use_case import (
    UpdateNotificationUseCase,
)
from notification_service.modules.notifications.domain.entities.notification import Notification
from notification_service.modules.notifications.presentation.http.schemas import (
    CreateNotificationBody,
    NotificationResponse,
    UpdateNotificationBody,
)

router = APIRouter(prefix="/notifications", tags=["notifications"], route_class=DishkaRoute)


@router.post("", response_model=NotificationResponse, status_code=201)
async def create(body: CreateNotificationBody, use_case: FromDishka[CreateNotificationUseCase]) -> Notification:
    return await use_case.execute(body.to_dto())


@router.get("", response_model=list[NotificationResponse])
async def list_items(
    use_case: FromDishka[ListNotificationsUseCase],
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    order_id: UUID | None = None,
) -> list[Notification]:
    return await use_case.execute(limit=limit, offset=offset, order_id=order_id)


@router.get("/{item_id}", response_model=NotificationResponse)
async def get(item_id: UUID, use_case: FromDishka[GetNotificationUseCase]) -> Notification:
    return await use_case.execute(item_id)


@router.put("/{item_id}", response_model=NotificationResponse)
async def update(
    item_id: UUID, body: UpdateNotificationBody, use_case: FromDishka[UpdateNotificationUseCase]
) -> Notification:
    return await use_case.execute(item_id, body.to_dto())


@router.delete("/{item_id}", status_code=204)
async def delete(item_id: UUID, use_case: FromDishka[DeleteNotificationUseCase]) -> Response:
    await use_case.execute(item_id)
    return Response(status_code=204)
