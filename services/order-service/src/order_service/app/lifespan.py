from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import AsyncContainer
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from order_service.core.db.database import metadata


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    container: AsyncContainer = app.state.dishka_container
    try:
        engine = await container.get(AsyncEngine)
        async with engine.begin() as connection:
            await connection.run_sync(metadata.create_all)
        yield
    finally:
        await container.close()
