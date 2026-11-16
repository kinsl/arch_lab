import logging
from typing import cast
from uuid import UUID

from sqlalchemy import Update, delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncConnection

from order_service.modules.orders.application.dto import UpdateOrderDTO
from order_service.modules.orders.domain.entities.order import NewOrder, Order
from order_service.modules.orders.domain.errors import ConflictError, NotFoundError
from order_service.modules.orders.domain.notification_status import NotificationStatus
from order_service.modules.orders.infrastructure.mappers.order_mapper import OrderMapper
from order_service.modules.orders.infrastructure.rows import OrderRow
from order_service.modules.orders.infrastructure.tables.orders import orders_table as table

logger = logging.getLogger(__name__)


class OrderRepository:
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def get(self, item_id: UUID) -> Order:
        row = (await self._connection.execute(select(table).where(table.c.id == item_id))).mappings().one_or_none()
        if row is None:
            raise NotFoundError("Order not found")
        return OrderMapper.to_entity(cast(OrderRow, row))

    async def list(self, *, limit: int, offset: int, order_id: UUID | None = None) -> list[Order]:
        statement = select(table).order_by(table.c.id).limit(limit).offset(offset)
        rows = (await self._connection.execute(statement)).mappings().all()
        return [OrderMapper.to_entity(cast(OrderRow, row)) for row in rows]

    async def add(self, data: NewOrder) -> Order:
        try:
            row = (
                (
                    await self._connection.execute(
                        insert(table)
                        .values(
                            user_id=data.user_id,
                            product=data.product,
                            quantity=data.quantity,
                            email=data.email,
                            notification_status=data.notification_status.value,
                        )
                        .returning(table)
                    )
                )
                .mappings()
                .one()
            )
            await self._connection.commit()
        except IntegrityError as exc:
            await self._connection.rollback()
            raise ConflictError("Conflicting order data") from exc
        return OrderMapper.to_entity(cast(OrderRow, row))

    async def update(self, item_id: UUID, data: UpdateOrderDTO) -> Order:
        statement = update(table).where(table.c.id == item_id).values(product=data.product, quantity=data.quantity)
        return await self._update(statement)

    async def set_notification_status(self, item_id: UUID, status: NotificationStatus) -> Order:
        statement = update(table).where(table.c.id == item_id).values(notification_status=status.value)
        return await self._update(statement)

    async def _update(self, statement: Update) -> Order:
        try:
            row = (await self._connection.execute(statement.returning(table))).mappings().one_or_none()
            if row is None:
                raise NotFoundError("Order not found")
            await self._connection.commit()
        except IntegrityError as exc:
            await self._connection.rollback()
            raise ConflictError("Conflicting data") from exc
        return OrderMapper.to_entity(cast(OrderRow, row))

    async def delete(self, item_id: UUID) -> None:
        result = await self._connection.execute(delete(table).where(table.c.id == item_id).returning(table.c.id))
        if result.scalar_one_or_none() is None:
            raise NotFoundError("Order not found")
        await self._connection.commit()
