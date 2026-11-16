from collections.abc import AsyncIterator

from dishka import AsyncContainer, Provider, Scope, from_context, make_async_container, provide
from httpx2 import AsyncClient, Timeout
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from order_service.app.config import Config
from order_service.core.db.database import get_engine
from order_service.modules.orders.di import OrderProvider


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

    @provide(scope=Scope.APP)
    async def client(self) -> AsyncIterator[AsyncClient]:
        async with AsyncClient(timeout=Timeout(2.0), trust_env=False) as client:
            yield client  # ruff:ignore[yield-in-context-manager-in-async-generator]


def create_container(config: Config) -> AsyncContainer:
    return make_async_container(AppProvider(), OrderProvider(), context={Config: config})
