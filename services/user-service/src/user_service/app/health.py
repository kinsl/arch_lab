from typing import Literal

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncEngine

router = APIRouter(tags=["health"], route_class=DishkaRoute)


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: Literal["user"]


@router.get("/health")
async def health(engine: FromDishka[AsyncEngine]) -> HealthResponse:
    async with engine.connect() as connection:
        await connection.exec_driver_sql("SELECT 1")
    return HealthResponse(status="ok", service="user")
