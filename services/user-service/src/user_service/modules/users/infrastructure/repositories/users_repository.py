import logging
from typing import cast
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncConnection

from user_service.modules.users.application.dto import CreateUserDTO, UpdateUserDTO
from user_service.modules.users.domain.entities.user import User
from user_service.modules.users.domain.errors import ConflictError, NotFoundError
from user_service.modules.users.infrastructure.mappers.user_mapper import UserMapper
from user_service.modules.users.infrastructure.rows import UserRow
from user_service.modules.users.infrastructure.tables.users import users_table as table

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def get(self, item_id: UUID) -> User:
        row = (await self._connection.execute(select(table).where(table.c.id == item_id))).mappings().one_or_none()
        if row is None:
            raise NotFoundError("User not found")
        return UserMapper.to_entity(cast(UserRow, row))

    async def list(self, *, limit: int, offset: int, order_id: UUID | None = None) -> list[User]:
        statement = select(table).order_by(table.c.id).limit(limit).offset(offset)
        rows = (await self._connection.execute(statement)).mappings().all()
        return [UserMapper.to_entity(cast(UserRow, row)) for row in rows]

    async def add(self, data: CreateUserDTO) -> User:
        try:
            row = (
                (
                    await self._connection.execute(
                        insert(table).values(name=data.name, email=data.email).returning(table)
                    )
                )
                .mappings()
                .one()
            )
            await self._connection.commit()
        except IntegrityError as exc:
            await self._connection.rollback()
            raise ConflictError("Email already exists") from exc
        return UserMapper.to_entity(cast(UserRow, row))

    async def update(self, item_id: UUID, data: UpdateUserDTO) -> User:
        try:
            row = (
                (
                    await self._connection.execute(
                        update(table)
                        .where(table.c.id == item_id)
                        .values(name=data.name, email=data.email)
                        .returning(table)
                    )
                )
                .mappings()
                .one_or_none()
            )
            if row is None:
                raise NotFoundError("User not found")
            await self._connection.commit()
        except IntegrityError as exc:
            await self._connection.rollback()
            raise ConflictError("Conflicting data") from exc
        return UserMapper.to_entity(cast(UserRow, row))

    async def delete(self, item_id: UUID) -> None:
        result = await self._connection.execute(delete(table).where(table.c.id == item_id).returning(table.c.id))
        if result.scalar_one_or_none() is None:
            raise NotFoundError("User not found")
        await self._connection.commit()
