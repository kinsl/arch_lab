from collections.abc import AsyncIterator

from dishka import AsyncContainer, Provider, Scope, from_context, make_async_container, provide
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from notification_service.app.config import Config
from notification_service.core.db.database import get_engine
from notification_service.modules.notifications.di import NotificationProvider


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def engine(self, config: Config) -> AsyncIterator[AsyncEngine]:
        engine = get_engine(config.database_url)
        try:
            yield engine
        finally:
            await engine.dispose()

    @provide(scope=Scope.REQUEST)
    async def connection(self, engine: AsyncEngine) -> AsyncIterator[AsyncConnection]:
        async with engine.connect() as connection:
            try:
                yield connection  # ruff:ignore[yield-in-context-manager-in-async-generator]
            finally:
                await connection.rollback()


def create_container(config: Config) -> AsyncContainer:
    return make_async_container(AppProvider(), NotificationProvider(), context={Config: config})
