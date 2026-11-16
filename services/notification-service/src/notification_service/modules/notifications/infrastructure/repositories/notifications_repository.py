from typing import cast
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncConnection

from notification_service.modules.notifications.application.dto import (
    CreateNotificationDTO,
    CreateNotificationResult,
    UpdateNotificationDTO,
)
from notification_service.modules.notifications.domain.entities.notification import Notification
from notification_service.modules.notifications.domain.errors import ConflictError, NotFoundError
from notification_service.modules.notifications.infrastructure.mappers.notification_mapper import (
    NotificationMapper,
)
from notification_service.modules.notifications.infrastructure.rows import NotificationRow
from notification_service.modules.notifications.infrastructure.tables.notifications import (
    notifications_table as table,
)


class NotificationRepository:
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def get(self, item_id: UUID) -> Notification:
        row = (await self._connection.execute(select(table).where(table.c.id == item_id))).mappings().one_or_none()
        if row is None:
            raise NotFoundError("Notification not found")
        return NotificationMapper.to_entity(cast(NotificationRow, row))

    async def list(self, *, limit: int, offset: int, order_id: UUID | None = None) -> list[Notification]:
        statement = select(table).order_by(table.c.id).limit(limit).offset(offset)
        if order_id is not None:
            statement = statement.where(table.c.order_id == order_id)
        rows = (await self._connection.execute(statement)).mappings().all()
        return [NotificationMapper.to_entity(cast(NotificationRow, row)) for row in rows]

    async def add(self, data: CreateNotificationDTO) -> CreateNotificationResult:
        statement = (
            insert(table)
            .values(order_id=data.order_id, email=data.email, message=data.message)
            .on_conflict_do_nothing(index_elements=[table.c.order_id])
            .returning(table)
        )
        row = (await self._connection.execute(statement)).mappings().one_or_none()
        if row is None:
            row = (
                (await self._connection.execute(select(table).where(table.c.order_id == data.order_id)))
                .mappings()
                .one()
            )
            if row["email"] != data.email or row["message"] != data.message:
                await self._connection.rollback()
                raise ConflictError("Different notification already exists for this order")
            await self._connection.commit()
            return CreateNotificationResult(
                notification=NotificationMapper.to_entity(cast(NotificationRow, row)), created=False
            )
        await self._connection.commit()
        return CreateNotificationResult(
            notification=NotificationMapper.to_entity(cast(NotificationRow, row)), created=True
        )

    async def update(self, item_id: UUID, data: UpdateNotificationDTO) -> Notification:
        try:
            row = (
                (
                    await self._connection.execute(
                        update(table)
                        .where(table.c.id == item_id)
                        .values(email=data.email, message=data.message)
                        .returning(table)
                    )
                )
                .mappings()
                .one_or_none()
            )
            if row is None:
                raise NotFoundError("Notification not found")
            await self._connection.commit()
        except IntegrityError as exc:
            await self._connection.rollback()
            raise ConflictError("Conflicting data") from exc
        return NotificationMapper.to_entity(cast(NotificationRow, row))

    async def delete(self, item_id: UUID) -> None:
        result = await self._connection.execute(delete(table).where(table.c.id == item_id).returning(table.c.id))
        if result.scalar_one_or_none() is None:
            raise NotFoundError("Notification not found")
        await self._connection.commit()
